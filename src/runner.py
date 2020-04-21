from time import time

from src.CBS import astar, CBS
from src.maze import Maze
from src.vizualizer import create_frame, create_gif

t = time()

maze = Maze.from_image("test_maze_5.png")

paths = CBS(maze)
create_gif("test.gif",maze,paths,20)

print(time()-t)