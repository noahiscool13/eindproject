class Corridor:
    def __init__(self, locs=None):
        if not locs:
            self.locs = {}
        else:
            self.locs = locs

def find_corridor_locs(grid,width,height):
    locs = {}
    for x in range(width):
        for y in range(height):
            c = 0

            if x == 0:
                c+=1
            if y == 0:
                c+=1


