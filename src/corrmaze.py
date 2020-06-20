import numpy as np

from src.CBS import CBS
from src.agent import Agent
from src.maze import Maze
from src.vizualizer import create_gif


def corrmaze(c_len):
    grid = np.zeros((3,c_len+2))
    for x in range(1,c_len+1):
        grid[0][x] = 1
        grid[2][x] = 1
    agents = [Agent("[255,0]",(0,0),(0,0),(c_len+1,0)),Agent("[0,255]",(c_len+1,2),(c_len+1,2),(0,2))]
    m = Maze(grid,agents)
    return m

if __name__ == '__main__':
    # for x in range(1,101):
    #     print(f"{x},",end="")
    #     m = corrmaze(x)
    #     s = CBS(m,False)
    m = corrmaze(1)
    s = CBS(m, False)
    # create_gif("cortest.gif", m, s, 50)