from collections import defaultdict

from src.maze import Maze


class MDD:
    def __init__(self, g):
        self.g = g

    def __len__(self):
        return len(self.g)

    @staticmethod
    def construct(maze, start, waypoints, goal, d, data, constraints=[]):
        from src.CBS import perfect_heuristic
        g = [{(start, frozenset(waypoints))}]
        per = [set()]
        for i in range(1, d):
            g.append(set())
            per.append(defaultdict(set))
            for p in g[-2]:
                for w in maze.reachable_from_posw(p[0]):
                    if (*w, i) not in constraints:
                        tf = p[1] - frozenset({w})
                        if perfect_heuristic((w,), goal, tf, data) < d - i:
                            g[-1].add((w, tf))
                            per[-1][w].add(p[0])

        t = [[goal]]
        for i in range(d - 1):
            t.append(set())
            for a in t[-2]:
                t[-1] |= per[-i - 1][a]
        g = t[::-1]
        return MDD(g)

    @staticmethod
    def merge(a, b):
        while len(a) < len(b):
            a.g.append(a.g[-1])
        while len(a) > len(b):
            b.g.append(b.g[-1])


if __name__ == '__main__':
    from src.CBS import flood_dists, Constraint

    maze = Maze.from_image("test_maze_26.png")

    dist_data = dict()
    for agent in maze.agents:
        dist_data[agent.goal] = flood_dists(maze, agent.goal)
        for waypoint in agent.waypoints:
            dist_data[waypoint] = flood_dists(maze, waypoint)

    compl_dists = dict()
    heuristic_data = {"direct": dist_data, "wp": compl_dists}

    agents = []
    for x in maze.agents:
        agents.append(x)

    # const = [Constraint(agent,((0,3),),1)]
    const = []
    agent = agents[0]
    mdd_a = MDD.construct(maze, agent.start, agent.waypoints, agent.goal, 5, heuristic_data, const)
    agent = agents[1]
    mdd_b = MDD.construct(maze, agent.start, agent.waypoints, agent.goal, 5, heuristic_data, const)

    print(MDD.merge(mdd_a, mdd_b).g)
