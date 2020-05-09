from collections import defaultdict


from src.maze import Maze


class MDD:
    def __init__(self,maze, start,waypoints, goal, d,data):
        from src.CBS import perfect_heuristic
        self.g = [{(start,frozenset(waypoints))}]
        for i in range(1,d):
            self.g.append(set())
            for p in self.g[-2]:
                for w in maze.reachable_from_posw(p[0]):
                    tf = p[1]-frozenset({w})
                    if perfect_heuristic((w,),goal,tf,data)<d-i:
                        self.g[-1].add((w,tf))
        for i in range(d):
            self.g[i] = {x[0] for x in self.g[i]}

if __name__ == '__main__':
    from src.CBS import flood_dists

    maze = Maze.from_image("test_maze_17.png")

    dist_data = dict()
    for agent in maze.agents:
        dist_data[agent.goal] = flood_dists(maze,agent.goal)
        for waypoint in agent.waypoints:
            dist_data[waypoint] = flood_dists(maze,waypoint)


    compl_dists = dict()
    heuristic_data = {"direct": dist_data, "wp": compl_dists}

    for x in maze.agents:
        agent = x
    mdd = MDD(maze,agent.start,agent.waypoints,agent.goal,10,heuristic_data)
    print(mdd.g)
