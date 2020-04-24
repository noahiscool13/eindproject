import numpy as np
from PIL import Image

from src.agent import Agent
from src.agentpool import AgentPool


class Maze:
    def __init__(self, grid, agents):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)

        self.agents = agents

    @staticmethod
    def name_from_pixel(pixel):
        return str(list(pixel[:2]))

    @staticmethod
    def from_image(file):
        img = Image.open(file)
        arr = np.array(img)
        height, width, _ = arr.shape
        grid = np.zeros((height,width),dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                if list(arr[y][x]) == [0,0,0,255]:
                    grid[y][x] = 1

        agents = AgentPool()
        for y in range(height):
            for x in range(width):
                if arr[y][x][2] == 16:
                    name = Maze.name_from_pixel(arr[y][x])
                    agents.add(Agent(name))
                    agents.get(name).set_start((x,y))

        for y in range(height):
            for x in range(width):
                if arr[y][x][2] == 80:
                    name = Maze.name_from_pixel(arr[y][x])
                    agents.get(name).add_waypoint((x,y))
                if arr[y][x][2] == 128:
                    name = Maze.name_from_pixel(arr[y][x])
                    agents.get(name).goal = (x,y)

        return Maze(grid,agents)
    
    def reachable_from(self,pos, constraints=None):
        if not constraints:
            constraints = []
        (x,y),t = pos
        t+=1
        out = []
        if x>0:
            if not self.grid[y][x-1]:
                if (x-1,y,t) not in constraints:
                    out.append(((x-1,y),t))
        if x+1<self.width:
            if not self.grid[y][x+1]:
                if (x+1,y,t) not in constraints:
                    out.append(((x+1,y),t))
        if y>0:
            if not self.grid[y-1][x]:
                if (x,y-1,t) not in constraints:
                    out.append(((x,y-1),t))
        if y+1<self.height:
            if not self.grid[y+1][x]:
                if (x,y+1,t) not in constraints:
                    out.append(((x,y+1),t))
        if (x, y, t) not in constraints:
            out.append(((x, y),t))
        return out

    def reachable_from_with_waypoints(self,pos, constraints=None):
        if not constraints:
            constraints = []
        (x,y),t,waypoints = pos
        t+=1
        out = []
        if x>0:
            if not self.grid[y][x-1]:
                if (x-1,y,t) not in constraints:
                    out.append(((x-1,y),t,waypoints-{(x-1,y)}))
        if x+1<self.width:
            if not self.grid[y][x+1]:
                if (x+1,y,t) not in constraints:
                    out.append(((x+1,y),t,waypoints-{(x+1,y)}))
        if y>0:
            if not self.grid[y-1][x]:
                if (x,y-1,t) not in constraints:
                    out.append(((x,y-1),t,waypoints-{(x,y-1)}))
        if y+1<self.height:
            if not self.grid[y+1][x]:
                if (x,y+1,t) not in constraints:
                    out.append(((x,y+1),t,waypoints-{(x,y+1)}))
        if (x, y, t) not in constraints:
            out.append(((x, y),t,waypoints))
        return out

    def reachable_from_with_cat(self,pos, constraints=None):
        if not constraints:
            constraints = []
        (x,y),t,waypoints,w = pos
        t+=1
        out = []
        if x>0:
            if not self.grid[y][x-1]:
                if (x-1,y,t) not in constraints:
                    out.append(((x-1,y),t,waypoints-{(x-1,y)},w))
        if x+1<self.width:
            if not self.grid[y][x+1]:
                if (x+1,y,t) not in constraints:
                    out.append(((x+1,y),t,waypoints-{(x+1,y)},w))
        if y>0:
            if not self.grid[y-1][x]:
                if (x,y-1,t) not in constraints:
                    out.append(((x,y-1),t,waypoints-{(x,y-1)},w))
        if y+1<self.height:
            if not self.grid[y+1][x]:
                if (x,y+1,t) not in constraints:
                    out.append(((x,y+1),t,waypoints-{(x,y+1)},w))
        if (x, y, t) not in constraints:
            out.append(((x, y),t,waypoints,w))
        return out

# Maze.from_image("test_maze_1.png")
