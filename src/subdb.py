import pickle

from src.vizualizer import create_gif

f = open("sub1","rb")
problem = pickle.load(f)
f.close()

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
    # create_gif("test4.gif", maze, paths, 20)
    print(paths.sum_of_individual_costs())
    # print([[y[0] for y in x.path] for x in paths])
    return [[y[0] for y in x.path] for x in paths]

print(solver(problem))