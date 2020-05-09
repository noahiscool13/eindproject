from time import time

from src.CBS import astar, CBS
from src.maze import Maze
from src.vizualizer import create_frame, create_gif

t = time()

maze = Maze.from_image("test_maze_20.png")

paths = CBS(maze)
create_gif("test2.gif",maze,paths,50)

print(time()-t)