from itertools import combinations

from math import inf


class Edge:
    def __init__(self, a1, a2, cost):
        self.agents = [a1, a2]
        self.cost = cost


class WGD:
    def __init__(self, agents):
        self.agents = agents
        self.edges = set()

    def add_edge(self, edge):
        self.edges.add(edge)

    def EWMVC(self):
        dagents = {}
        dagentscover = {}
        for x in self.agents:
            if any(x in e.agents for e in self.edges):
                dagents[x] = 0
                dagentscover[x] = set()
        for e in self.edges:
            dagents[e.agents[0]] += e.cost
            dagents[e.agents[1]] += e.cost

            dagentscover[e.agents[0]].add(e)
            dagentscover[e.agents[1]].add(e)

        best = inf
        for am in range(1, len(dagents) + 1):
            for c in combinations(dagents, am):
                cofered = set()
                for a in c:
                    cofered |= dagentscover[a]
                if cofered == self.edges:
                    cost = sum(dagents[a] for a in c)
                    best = min(best, cost)

        return best


if __name__ == '__main__':
    g = WGD([1, 2, 3, 4])
    g.add_edge(Edge(1, 2, 3))
    g.add_edge(Edge(2, 3, 4))
    g.add_edge(Edge(3, 1, 2))
    print(g.EWMVC())
