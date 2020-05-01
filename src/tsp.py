import time

import numpy as np
from math import inf

dists = {1:{1:0,2:5,3:2,4:8},
         2:{1:5,2:0,3:6,4:1},
         3:{1:2,2:6,3:0,4:4},
         4:{1:8,2:1,3:4,4:0}}

def tdp(start, waypoints, goal, data):
    """
    Traveling duck problem :)
    """
    if (start,waypoints,goal) in data["wp"]:
        return data["wp"][(start,waypoints,goal)]
    print(len(waypoints))
    memo = {((start,),start):0}
    # for p in waypoints:
    #     memo[] = dists["direct"][p][start]
    queue = [((start,),start)]
    # for p in waypoints:
    #     queue.append(((p,),p))
    while queue:
        cur_v, cur_p = queue.pop(0)
        cur_d = memo[(cur_v,cur_p)]
        open_points = waypoints-set(cur_v)-set(start)
        for nxt_p in open_points:
            nxt_v = tuple(sorted(list(cur_v) + [nxt_p]))
            nxt_d = cur_d + data["direct"][nxt_p][cur_p]
            nxt_t = (nxt_v,nxt_p)
            if nxt_t not in memo:
                memo[nxt_t] = nxt_d
                queue.append((nxt_v,nxt_p))
            else:
                if nxt_d<memo[nxt_t]:
                    memo[nxt_t]=nxt_d
    b = inf
    waypoints = tuple(sorted(waypoints))
    for p in waypoints:
        if p != start:
            t = memo[(waypoints,p)] + data["direct"][goal][p]
            if t<b:
                b = t
    print(b)
    data["wp"][(start, frozenset(waypoints), goal)] = b
    return b

# tdp(1,{2,3},4,dists)

def DP_TSP(distances_array):
    n = len(distances_array)
    all_points_set = set(range(n))

    # memo keys: tuple(sorted_points_in_path, last_point_in_path)
    # memo values: tuple(cost_thus_far, next_to_last_point_in_path)
    memo = {(tuple([i]), i): tuple([0, None]) for i in range(n)}
    queue = [(tuple([i]), i) for i in range(n)]

    while queue:
        prev_visited, prev_last_point = queue.pop(0)
        prev_dist, _ = memo[(prev_visited, prev_last_point)]

        to_visit = all_points_set.difference(set(prev_visited))
        for new_last_point in to_visit:
            new_visited = tuple(sorted(list(prev_visited) + [new_last_point]))
            new_dist = prev_dist + distances_array[prev_last_point][new_last_point]

            if (new_visited, new_last_point) not in memo:
                memo[(new_visited, new_last_point)] = (new_dist, prev_last_point)
                queue += [(new_visited, new_last_point)]
            else:
                if new_dist < memo[(new_visited, new_last_point)][0]:
                    memo[(new_visited, new_last_point)] = (new_dist, prev_last_point)

    optimal_path, optimal_cost = retrace_optimal_path(memo, n)

    return optimal_path, optimal_cost

def retrace_optimal_path(memo: dict, n: int) -> [[int], float]:
    points_to_retrace = tuple(range(n))

    full_path_memo = dict((k, v) for k, v in memo.items() if k[0] == points_to_retrace)
    path_key = min(full_path_memo.keys(), key=lambda x: full_path_memo[x][0])

    last_point = path_key[1]
    optimal_cost, next_to_last_point = memo[path_key]

    optimal_path = [last_point]
    points_to_retrace = tuple(sorted(set(points_to_retrace).difference({last_point})))

    while next_to_last_point is not None:
        last_point = next_to_last_point
        path_key = (points_to_retrace, last_point)
        _, next_to_last_point = memo[path_key]

        optimal_path = [last_point] + optimal_path
        points_to_retrace = tuple(sorted(set(points_to_retrace).difference({last_point})))

    return optimal_path, optimal_cost

def generate_random_input(n_points):
    X = np.random.rand(n_points, 2)
    distances_array = np.array([[np.linalg.norm(X[i] - X[j])
                                 for i in range(n_points)]
                                for j in range(n_points)])
    return X, distances_array

# input_size = 4
# X, distances_array = generate_random_input(input_size)
#
# t = time.time()
# optimal_path, optimal_cost = DP_TSP(distances_array)
# runtime = round(time.time() - t, 3)
#
# print(f"Found optimal path in {runtime} seconds.")
# print(f"Optimal cost: {round(optimal_cost, 3)}, optimal path: {optimal_path}")