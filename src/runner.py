from time import time

from src.CBS import astar, CBS
from src.maze import Maze
from src.vizualizer2 import create_frame, create_gif

maze = Maze.from_image("test_maze_27.png")

t = time()

for x in range(1):
    paths = CBS(maze)

print(time() - t)

create_gif("test.gif", maze, paths, 10,)
