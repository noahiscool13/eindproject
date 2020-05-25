from copy import deepcopy
from queue import PriorityQueue

from math import inf


class AdjMat:
    def __init__(self, mat):
        self.mat = mat
        self.size = len(mat)

    def redu(self):
        c = 0
        for row in range(self.size):
            v = min(self.mat[row])
            if v != inf:
                c+=v
                for col in range(self.size):
                    self.mat[row][col]-=v

        for col in range(self.size):
            v = min(x[col] for x in self.mat)
            if v != inf:
                c+=v
                for row in range(self.size):
                    self.mat[row][col]-=v

        return c

    def __str__(self):
        return "\n".join(str(x) for x in self.mat)

class State:
    def __init__(self,mat,pos,cost=0,depth=0):
        self.mat = mat
        self.pos = pos
        self.cost = cost
        self.depth = depth

    def __lt__(self, other):
        return self.cost<other.cost

    def legal(self):
        found = []
        for x in range(self.mat.size):
            if self.mat.mat[self.pos][x] != inf:
                found.append(x)
        return found

    def move(self, pos):
        new_mat = deepcopy(self.mat)
        for x in range(self.mat.size):
            new_mat.mat[self.pos][x] = inf
            new_mat.mat[x][pos] = inf
        new_mat.mat[pos][0] = inf
        a,b,c = self.mat.mat[self.pos][pos],self.cost,new_mat.redu()
        c = a+b+c

        return State(new_mat,pos,c,self.depth+1)

    def __str__(self):
        return f"Cost: {self.cost}, Pos: {self.pos}\n"+str(self.mat)



def tsp(state):
    q = PriorityQueue()
    q.put((state.cost,state))

    # print(state)

    while q:
        s = q.get()[1]
        if s.depth == s.mat.size-1:
            return s.cost
        c = s.legal()

        for x in c:
            n = s.move(x)

            # print(n)
            # print()

            q.put((n.cost-n.depth/10000,n))


def tdp(start, waypoints, goal, data):
    """
        Traveling duck problem :)
        """
    if (start, waypoints, goal) in data["wp"]:
        return data["wp"][(start, waypoints, goal)]
    print(len(waypoints))

    waypoints = list(waypoints)

    adj = []
    for x in waypoints:
        t = []
        for y in waypoints:
            if x==y:
                t.append(inf)
            else:
                t.append(data["direct"][x][y])
        t.append(data["direct"][x][goal])
        adj.append(t)
    t = []
    for x in waypoints:
        if x == start:
            t.append(0)
        else:
            t.append(inf)
    t.append(inf)
    adj.append(t)

    adj = AdjMat(adj)
    c = adj.redu()

    s = State(adj, 0, c)

    dist = tsp(s)

    data["wp"][(start, frozenset(waypoints), goal)] = dist
    # print(dist)
    return dist

if __name__ == '__main__':
    mat = [
        [inf,20,30,10,11],
        [15,inf,16,4,2],
        [3,5,inf,2,4],
        [19,6,18,inf,3],
        [16,4,7,16,inf]
    ]

    adj = AdjMat(mat)
    c = adj.redu()

    s = State(adj,0,c)

    print(tsp(s))

