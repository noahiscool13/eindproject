from src.CBS import astar, CBS
from src.maze import Maze
from src.vizualizer import create_frame, create_gif

maze = Maze.from_image("test_maze_3.png")

paths = CBS(maze)
paths.print_solution()
create_gif("test.gif",maze,paths,100)