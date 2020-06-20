from queue import Queue
from time import time

from math import inf


def tdp(start, waypoints, goal, data):
    """
    Traveling duck problem :)
    """

    if (start,waypoints,goal) in data["wp"]:
        return data["wp"][(start,waypoints,goal)]

    # print(len(waypoints), end=" ")
    # if len(waypoints) in [13] or 1:
    #     timer = time()
    # print(len(waypoints))
    memo = {((waypoint,),waypoint):data["direct"][goal][waypoint] for waypoint in waypoints}
    # memo = {((start,),start):0}
    # for p in waypoints:
    #     memo[] = dists["direct"][p][start]
    queue = Queue()
    for waypoint in waypoints:
        queue.put(((waypoint,),waypoint))
    # queue = [((waypoint,),waypoint) for waypoint in waypoints]
    # queue = [((start,),start)]
    # for p in waypoints:
    #     queue.append(((p,),p))
    while not queue.empty():
        # cur_v, cur_p = queue.pop(0)
        cur_v, cur_p = queue.get()

        # cur_v, cur_p = queue[0]
        # queue = queue[1:]
        cur_d = memo[(cur_v,cur_p)]
        open_points = waypoints-set(cur_v)
        for nxt_p in open_points:
            nxt_v = tuple(sorted(list(cur_v) + [nxt_p]))
            nxt_d = cur_d + data["direct"][nxt_p][cur_p]
            nxt_t = (nxt_v,nxt_p)
            if nxt_t not in memo:
                memo[nxt_t] = nxt_d
                # queue.append((nxt_v,nxt_p))
                queue.put((nxt_v,nxt_p))

            else:
                if nxt_d<memo[nxt_t]:
                    memo[nxt_t]=nxt_d
    # b = inf
    # waypoints = tuple(sorted(waypoints))
    # for p in waypoints:
    #     if p != start:
    #         t = memo[(waypoints,p)] + data["direct"][goal][p]
    #         if t<b:
    #             b = t

    waypoints = tuple(sorted(waypoints))
    for p in waypoints:
        data["wp"][(p, frozenset(waypoints), goal)] = memo[(waypoints,p)]

    # if len(waypoints) in [13] or 1:
    #     print(time()-timer)
    return data["wp"][(start, frozenset(waypoints), goal)]