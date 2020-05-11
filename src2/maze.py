import numpy as np
from PIL import Image

from src2.agent import Agent
from src2.agentpool import AgentPool


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

        return Maze(grid.tolist(),agents)