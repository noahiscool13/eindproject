from random import choice, sample


class GD:
    def __init__(self,agents):
        self.nodes = agents
        self.edges = set()

    def fmvc(self):
        h = 0
        ec = self.edges

        while ec:
            h+=1
            n = sample(self.edges,1)[0]
            ne = set()
            for e in ec:
                if e[0]!=n[0] and e[1]!=n[0] and e[0]!=n[1] and e[1]!=n[1]:
                    ne.add(e)
            ec = ne

        return h

if __name__ == '__main__':
    g = GD([1,2,3,4])
    g.edges = set([(0,1),(2,3)])
    print(g.fmvc())