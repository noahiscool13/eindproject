from copy import deepcopy



class Corridor:
    def __init__(self, locs=None):
        if not locs:
            self.locs = {}
        else:
            self.locs = locs
        self.a = None
        self.b = None
        self.order = None

    def closest(self,loc):
        ind = self.order.index(loc[0])
        if ind<len(self.order)-ind-1:
            return (self.a,self.b)
        return (self.b,self.a)

    def div(self,loc_1,loc_2):
        if loc_1[0] not in self.order:
            return self.closest(loc_2)
        if loc_2[0] not in self.order:
            return self.closest(loc_1)
        ind1 = self.order.index(loc_1[0])
        ind2 = self.order.index(loc_2[0])
        if ind1<ind2:
            return (self.a, self.b)
        return (self.b, self.a)

    def delta(self,loc):
        ind = self.order.index(loc[0])
        return min(ind,len(self.order)-ind-1)

    def find_order(self):
        self.order = [self.a]
        cp = list(self.locs)
        cp.remove(self.a)
        while cp:
            loc = self.order[-1]
            for l in cp:
                if loc[0] + 1 == l[0] and loc[1] == l[1]:
                    cp.remove(l)
                    self.order.append(l)
                    continue
                if loc[0] - 1 == l[0] and loc[1] == l[1]:
                    cp.remove(l)
                    self.order.append(l)
                    continue
                if loc[0] == l[0] and loc[1] + 1 == l[1]:
                    cp.remove(l)
                    self.order.append(l)
                    continue
                if loc[0] == l[0] and loc[1] - 1 == l[1]:
                    cp.remove(l)
                    self.order.append(l)
                    continue

    def find_ab(self):
        ab = []
        for loc in self.locs:
            c = 0
            for l in self.locs:
                if loc[0] + 1 == l[0] and loc[1] == l[1]:
                    c+=1
                if loc[0] - 1 == l[0] and loc[1] == l[1]:
                    c+=1
                if loc[0] == l[0] and loc[1] + 1 == l[1]:
                    c+=1
                if loc[0] == l[0] and loc[1] - 1 == l[1]:
                    c+=1
            if c == 1:
                ab.append(loc)
        self.a,self.b = ab

    def borders(self, loc):
        for l in self.locs:
            if loc[0]+1==l[0] and loc[1]==l[1]:
                return True
            if loc[0]-1==l[0] and loc[1]==l[1]:
                return True
            if loc[0]==l[0] and loc[1]+1==l[1]:
                return True
            if loc[0]==l[0] and loc[1]-1==l[1]:
                return True
        return False

    def __len__(self):
        return len(self.locs)

    def __contains__(self, item):
        return item in self.locs

    def __iter__(self):
        return iter(self.locs)

    def __str__(self):
        return f"<Corridor: {self.order}, s/e: {self.a}, {self.b}>"

def find_corridor_locs(maze):
    grid = maze.grid
    width = maze.width
    height = maze.height

    key_points = set()
    for agent in maze.agents:
        key_points.add(agent.start)
        key_points.add(agent.goal)
        for wp in agent.waypoints:
            key_points.add(wp)

    locs = set()
    for x in range(width):
        for y in range(height):
            if (not grid[y][x]) and ((x,y) not in key_points):
                c = 0
                if x>0:
                    if grid[y][x-1]:
                        c+=1
                else:
                    c+=1

                if y > 0:
                    if grid[y-1][x]:
                        c += 1
                else:
                    c += 1

                if x + 1 < width:
                    if grid[y][x+1]:
                        c += 1
                else:
                    c += 1

                if y + 1 < height:
                    if grid[y + 1][x]:
                        c += 1
                else:
                    c += 1

                if c>=2:
                    locs.add((x,y))
    return locs


def fuse(hits):
    t = set()
    for x in hits:
        t|=x.locs
    return Corridor(t)


def merge(locs):
    paths = []
    for l in locs:
        hits = [Corridor({l})]
        np = paths[:]
        for path in paths:
            if path.borders(l):
                hits.append(path)
                np.remove(path)
        np.append(fuse(hits))
        paths = np
    paths = [path for path in paths if len(path)>2]
    for x in paths:
        x.find_ab()
        x.find_order()
    return paths

def find_cor_wide(lst, pos):
    for x in lst:
        if pos in x:
            return x

def find_cor(lst, pos):
    for x in lst:
        if x.a == pos:
            return (x,x.a,x.b)
        if x.b == pos:
            return (x,x.b,x.a)
    return False

def to_print(grid,cors):
    g = grid.tolist()

    for c in cors:
        for x in c:
            grid[x[1]][x[0]] = 2
            g[x[1]][x[0]] = 2
    out = []
    for x in g:
        out.append("".join(str(n) for n in x).replace("0"," ").replace("1","X").replace("2","o"))
    print("\n".join(out))

if __name__ == '__main__':
    from src.maze import Maze

    maze = Maze.from_image("test_maze_28.png")

    p = find_corridor_locs(maze)

    pts = merge(p)

    print(pts)
    for x in pts:
        print(x)
    print(len(pts))
    print(list(len(x) for x in pts))

    to_print(maze.grid,pts)

