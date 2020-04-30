from mapfw import MapfwBenchmarker

from src.CBS import CBS
from src.agent import Agent
from src.maze import Maze

benchmarker = MapfwBenchmarker("13",5,"CBS","perfect_heuristic",False)
for problem in benchmarker:
    n_agents = len(problem.starts)
    agents = [Agent(f"[{x * 347 % 256},{x * 9231 % 256}]", tuple(problem.starts[x]), tuple(problem.starts[x]),
                    tuple(problem.goals[x]), set(tuple(n) for n in problem.waypoints[x])) for x in
              range(n_agents)]
    maze = Maze(problem.grid, agents)

    paths = CBS(maze)

    problem.add_solution([[y[0] for y in x.path] for x in paths])
