from mapfw import MapfwBenchmarker, get_all_benchmarks



def solver(problem):
    from src.CBS import CBS
    from src.agent import Agent
    from src.maze import Maze
    # print(problem)
    n_agents = len(problem.starts)
    agents = [Agent(f"[{x * 347 % 256},{x * 9231 % 256}]", tuple(problem.starts[x]), tuple(problem.starts[x]),
                    tuple(problem.goals[x]), set(tuple(n) for n in problem.waypoints[x])) for x in
              range(n_agents)]
    maze = Maze(problem.grid, agents)

    paths = CBS(maze, False)
    # print([[y[0] for y in x.path] for x in paths])
    return [[y[0] for y in x.path] for x in paths]

def main():

    benchmarker = MapfwBenchmarker("8E475BB3EDaaFc0e",(70), "CBS", "prog_test", False, solver=solver,cores=4)
    # benchmarker = MapfwBenchmarker("b76d216Ac99EbA4E",(70,), "CBS", "WDG_wip", False, solver=solver)
    benchmarker.run()
# for problem in benchmarker:
#     print(problem)
#     n_agents = len(problem.starts)
#     agents = [Agent(f"[{x * 347 % 256},{x * 9231 % 256}]", tuple(problem.starts[x]), tuple(problem.starts[x]),
#                     tuple(problem.goals[x]), set(tuple(n) for n in problem.waypoints[x])) for x in
#               range(n_agents)]
#     maze = Maze(problem.grid, agents)
#
#     paths = CBS(maze,False)
#     print([[y[0] for y in x.path] for x in paths])
#     problem.add_solution([[y[0] for y in x.path] for x in paths])




# class Agent:
#     def __init__(self, start, goal, waypoints):
#         self.start = start
#         self.goal = goal
#         self.waypoints = waypoints
#
#
# class Maze:
#     def __init__(self, grid, width, height):
#         self.grid = grid
#         self.width = width
#         self.height = height
#
#
# def solve(problem):
#      number_of_agents = len(problem.starts)
#     agents = []
#     for i in range(number_of_agents):
#         agents.append(Agent(problem.starts[i], problem.starts[i], problem.goals[i], problem.waypoints[i]))
#     maze = Maze(problem.grid, problem.width, problem.height)
#
#     paths = []
#     for agent in agents:
#         paths.append(find_path(agent, maze))
#
#     """
#     Now paths looks like:
#
#     paths = [path agent 1, path agent 2, ..]
#     path agent 1 = [pos agent 1 at time 0, pos agent 1 at time 1, .., pos agent 1 at finishing time]
#     pos = [x coordinate, y coordinate]
#     """
#
#     return paths
#
#
# from mapfw import MapfwBenchmarker
#
# benchmarker = MapfwBenchmarker("<YOUR API TOKEN>", <BENCHMARK INDEX>, "<YOUR ALGORITHMS NAME>",
#                                "<YOUR ALGORITHMS VERSION>", <DEBUG_MODE>)
# for problem in benchmarker:
#     problem.add_solution(solve(problem))
