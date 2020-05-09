import json
from time import time

import requests

from src.CBS import CBS
from src.agent import Agent
from src.maze import Maze


class Problem:
    def __init__(self, grid, width, height, starts, goals, waypoints, benchmark, id, batch_pos):
        self.grid = grid
        self.width = width
        self.height = height
        self.starts = starts
        self.goals = goals
        self.waypoints = waypoints
        self.benchmark = benchmark
        self.id = id
        self.batch_pos = batch_pos
        self.start_time = time()
        self.time = 0

    def __str__(self):
        out = f"<Problem\n" \
            f"\tWidth: {self.width}\n" \
            f"\tHeight: {self.height}\n" \
            f"\tStarts: {self.starts}\n" \
            f"\tGoals: {self.goals}\n" \
            f"\tGrid:\n"
        out += "\n".join("\t" + "".join(" " if it == 0 else "X" for it in row) for row in self.grid)
        out += "\n>"
        return out

    def add_solution(self, paths):
        """
        Add the solution to the problem

        paths = [path agent 1, path agent 2, ..]
        path agent 1 = [pos agent 1 at time 0, pos agent 1 at time 1, .., pos agent 1 at finishing time]
        pos = [x coordinate, y coordinate]

        :param paths: list of paths that the agents take
        """
        assert self.benchmark.status["state"] == "RUNNING", print(
            f"Benchmark seems to be inactive. state: {self.benchmark.status(['state'])}")
        assert self.benchmark.status["data"]["problem_states"][self.batch_pos] == 0, print(
            "Problem seems to be already solved")

        self.paths = paths
        self.time = time()-self.start_time
        self.benchmark.status["data"]["problem_states"][self.batch_pos] = 1

        if all(self.benchmark.status["data"]["problem_states"]):
            self.status = {"state": "SUBMITTING", "data": None}
            self.benchmark.submit()

    @staticmethod
    def from_json(data, benchmark, batch_pos):
        problem_part = json.loads(data["problem"])
        return Problem(problem_part["grid"], problem_part["width"], problem_part["height"], problem_part["starts"],
                       problem_part["goals"], problem_part["waypoints"], benchmark, data["id"], batch_pos)


class MapfwBenchmarker:
    def __init__(self, token: str, problem_id: int, algorithm: str, version: str):
        """
        Helper function to handle API requests

        :param token:
        :param benchmark:
        :param algorithm:
        :param version:
        """
        self.token = token
        self.algorithm = algorithm
        self.version = version
        self.problem_id = problem_id
        self.problems = None
        self.status = {"state": "UNINITIALIZED", "data": None}
        self.attempt_id = None

    def __iter__(self):
        for problem in self.problems:
            problem.start_time = time()
            yield problem

    def submit(self):
        headers = {
            'X-API-Token': self.token
        }

        data = {
            "solutions": [
                {
                    "problem": problem.id,
                    "time": round(problem.time * 1000),
                    "solution": problem.paths
                }
            ] for problem in self.problems
        }

        r = requests.post(f"https://mapfw.nl/api/attempts/{self.attempt_id}/solutions", headers=headers, json=data)
        assert r.status_code == 200, print(r.content)

        self.status = {"state": "SUBMITTED", "data": None}

    def load(self):
        assert self.status["state"] == "UNINITIALIZED", print("The benchmark seems to already been initialized\n")

        headers = {
            'X-API-Token': self.token
        }

        data = {
            "algorithm": self.algorithm,
            "version": self.version
        }

        r = requests.post(f"https://mapfw.nl/api/benchmarks/{self.problem_id}/problems", headers=headers, json=data)

        assert r.status_code == 200, print(r.content)

        self.problems = [Problem.from_json(part, self, pos) for pos, part in enumerate(r.json()["problems"])]
        self.attempt_id = r.json()["attempt"]

        self.status = {"state": "RUNNING", "data": {"problem_states": [0 for _ in self.problems]}}


if __name__ == '__main__':
    benchmark = MapfwBenchmarker("13", 4, "test", "api")
    benchmark.load()


    for problem in benchmark:
        print(benchmark.problems)
        n_agents = len(problem.starts)
        agents = [Agent(f"[{x * 347 % 256},{x * 9231 % 256}]", tuple(problem.starts[x]), tuple(problem.starts[x]),
                        tuple(problem.goals[x]), set(tuple(n) for n in problem.waypoints[x])) for x in
                  range(n_agents)]
        maze = Maze(problem.grid, agents)

        paths = CBS(maze)

        problem.add_solution([[y[0] for y in x.path] for x in paths])
