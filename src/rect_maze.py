from itertools import product
from random import randint
from time import time

import numpy as np
from func_timeout import func_timeout, FunctionTimedOut
from math import floor

from src.CBS import CBS
from src.agent import Agent
from src.maze import Maze
from src.vizualizer import create_gif

from matplotlib import pyplot as plt
import matplotlib

from random import choice



def rect(size, n_agents, dens):
    valid = 0
    while not valid:
        grid = np.zeros(size)
        locs = list(product(range(size[0]), range(size[1])))

        blocks = floor(size[0] * size[1] * dens)

        for _ in range(blocks):
            r = randint(0, len(locs) - 1)
            grid[locs[r][1]][locs[r][0]] = 1
            del locs[r]

        tm = Maze(grid, [])

        agents = []
        for i in range(n_agents):
            r = randint(0, len(locs) - 1)
            start = locs[r]
            del locs[r]

            end = start
            if tm.reachable_from_pos(end):
                for _ in range(5000):
                    end = choice(tm.reachable_from_pos(end))
                for _ in range(100):
                    if end in locs:
                        break
                    end = choice(tm.reachable_from_pos(end))
                if end not in locs:
                    continue
                locs.remove(end)

            agents.append(Agent(f"[{i * 347 % 256},{i * 9231 % 256}]", start, start, end))
            valid = 1

    return Maze(grid, agents)


def test(setings):
    # m = rect((8, 8), setings[0],0.15)
    try:
        cf = func_timeout(500, CBS, args=(setings[0], setings[1]))
        return 1
    except FunctionTimedOut:
        return 0
    except Exception as e:
        print(e)


if __name__ == '__main__':
    from multiprocessing import Pool
    matplotlib.use("TkAgg")


    # m = rect((8, 8), 15, 0.15)
    # s = CBS(m,True)
    # create_gif("blocktest.gif", m, s, 50)

    pcl = []
    npcl = []
    datapoints = list(range(5,6,1))
    t = time()
    for d in datapoints:
        maps = [rect((8, 8), d,0.15) for _ in range(3)]
        print(d)
        with Pool() as p:
            r = p.map(test, [(map,True) for map in maps])
            pcl.append(sum(r))
        print(time()-t,sum(r))

        print(d)
        with Pool() as p:
            r = p.map(test, [(map,False) for map in maps])
            npcl.append(sum(r))
        print(time() - t, sum(r))


    plt.plot(datapoints,pcl,label="pc")
    plt.plot(datapoints, npcl,label="npc")
    plt.legend()
    plt.show()
    # create_gif("blocktest.gif", m, s, 50)
