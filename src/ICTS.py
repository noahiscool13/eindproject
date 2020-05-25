from src.CBS import flood_dists, solve
from src.MDD import MDD
from src.maze import Maze


class Budget:
    def __init__(self,budgets):
        self.budgets = budgets

    def children(self):
        for x in range(len(self.budgets)):
            new_budgets = list(self.budgets)
            new_budgets[x]+=1
            yield Budget(tuple(new_budgets))

    def __getitem__(self, item):
        return self.budgets[item]

    def __hash__(self):
        h = hash(self.budgets)
        return h

    def __eq__(self, other):
        return self.budgets == other.budgets

    def __str__(self):
        return f"<{' '.join(str(x) for x in self.budgets)}>"


def generator(layer):
    for x in layer:
        yield x
    # for x in range(20):
    while 1:
        newlayer = set()
        for x in layer:
            for c in x.children():
                newlayer.add(c)
        layer = newlayer
        for x in layer:
            yield x




def ICTS(maze):
    dist_data = dict()
    for agent in maze.agents:
        dist_data[agent.goal] = flood_dists(maze, agent.goal)
        for waypoint in agent.waypoints:
            dist_data[waypoint] = flood_dists(maze, waypoint)

    compl_dists = dict()
    heuristic_data = {"direct":dist_data,"wp":compl_dists}

    paths = solve(maze,[],data=heuristic_data)
    startingbudget = Budget(list(len(path) for path in paths))

    for x in generator([startingbudget]):
        print(x)
        mdd = MDD.construct(maze, maze.agents[0].start, maze.agents[0].waypoints, maze.agents[0].goal, x[0] , heuristic_data, [])
        c = 0
        for a in maze.agents[1:]:
            c+=1
            nmdd = MDD.construct(maze, a.start, a.waypoints, a.goal, x[c] , heuristic_data, [])
            mdd = MDD.merge(mdd,nmdd,True)
        if mdd:

            c = list(mdd.g[-1])[0]

            p = [c]

            for x in range(len(mdd.p)-1,-1,-1):
                p.append(mdd.p[x][p[-1]])
            p = list(zip(*p[::-1]))
            print(p)
            return p

if __name__ == '__main__':
    maze = Maze.from_image("test_maze_13.png")
    mdd = ICTS(maze)
    print(mdd)
