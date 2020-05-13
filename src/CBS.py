from collections import defaultdict
from copy import deepcopy

from math import inf, atan, pi

from src.GD import GD
from src.MDD import MDD
from src.agent import Agent

from itertools import chain, combinations, permutations

from src.tsp import tdp


def fast_min(a,b):
    return a if a<b else b

def min_test(it,key):
    return min(it,key=key)

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def constant_factory(value):
    return lambda: value


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]

def tsp(p,waypoints,goal,data):
    if (p,waypoints,goal) in data["wp"]:
        return data["wp"][(p,waypoints,goal)]

    rest = (point for point in waypoints if point != p)
    best = inf
    for perm in permutations(rest):
        d = 0
        cp = p
        for tp in perm:
            d+=data["direct"][tp][cp]
            cp = tp
        d+=data["direct"][goal][cp]
        best = fast_min(best,d)
    data["wp"][(p,frozenset(waypoints),goal)] = best
    return best

def perfect_heuristic(pos, goal, waypoints, data):
    sp = pos[0]
    if not waypoints:
        return data["direct"][goal][sp]
    if len(waypoints) == 1:
        return data["direct"][list(waypoints)[0]][sp]+data["direct"][goal][list(waypoints)[0]]
    best = inf
    for p in waypoints:
        d = data["direct"][p][sp]
        d+= tdp(p,frozenset(waypoints),goal,data)
        best = fast_min(best,d)
    return best

def manhatan(pos, goal):
    return abs(pos[0][0] - goal[0]) + abs(pos[0][1] - goal[1])

def waypointheuristic(pos, goal, waypoints):
    if not waypoints:
        return manhatan(pos, goal)
    furtherst = max(waypoints, key=lambda waypoint: manhatan(pos, waypoint))
    return manhatan(pos, furtherst) + len(waypoints) - 1 + manhatan((furtherst, 0), goal)


def astar(maze, start, goal, h, constraints=None):
    open_set = {(start, 0)}
    came_from = dict()
    gscore = defaultdict(constant_factory(inf))
    gscore[(start, 0)] = 0
    fscore = defaultdict(constant_factory(inf))
    fscore[(start, 0)] = h((start, 0), goal)

    while open_set:
        current = min(open_set, key=lambda x: fscore[x])
        if current[0] == goal:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        for neighbor in maze.reachable_from(current, constraints=constraints):
            tentative_gscore = gscore[current] + 1
            if tentative_gscore < gscore[neighbor]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_gscore
                fscore[neighbor] = tentative_gscore + h(neighbor, goal)
                open_set.add(neighbor)

    # print("NO PATH FOUND!!")
    return None


def astarwp(maze, start, goal, waypoints, h, constraints=None):
    if (start[0], start[1], 0) in constraints:
        return None

    start_state = (start, 0, frozenset(waypoints))
    open_set = {start_state}
    came_from = dict()
    gscore = defaultdict(constant_factory(inf))
    gscore[start_state] = 0
    fscore = defaultdict(constant_factory(inf))
    fscore[start_state] = h(start_state, goal, waypoints)

    while open_set:
        current = min(open_set, key=lambda x: fscore[x])
        if current[0] == goal and not current[2]:
            if not constraints or current[1] >= max(constraints, key=lambda x: x.time).time:
                return reconstruct_path(came_from, current)

        open_set.remove(current)
        for neighbor in maze.reachable_from_with_waypoints(current, constraints=constraints):
            tentative_gscore = gscore[current] + 1
            if tentative_gscore < gscore[neighbor]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_gscore
                fscore[neighbor] = tentative_gscore + h(neighbor, goal, waypoints)
                open_set.add(neighbor)

    # print("NO PATH FOUND!!")
    return None

def astarwpcat(maze,agent, start, goal, waypoints, h, upper, constraints=None):
    if (start[0], start[1], 0) in constraints:
        return None

    start_state = (start, 0, frozenset(waypoints))
    open_set = {start_state}
    came_from = dict()
    gscore = defaultdict(constant_factory(inf))
    gscore[start_state] = 0
    fscore = defaultdict(constant_factory(inf))
    fscore[start_state] = h(start_state, goal, waypoints)

    while open_set:
        current = min(open_set, key=lambda x: fscore[x])
        if current[0] == goal and not current[2]:
            if not constraints or current[1] >= max(constraints, key=lambda x: x.time).time:
                return reconstruct_path(came_from, current)

        open_set.remove(current)
        for neighbor in maze.reachable_from_with_waypoints(current, constraints=constraints):
            cat_hit = 0
            for path in upper.solution:
                if agent == path.agent:
                    continue
                if path[fast_min(neighbor[1], len(path) - 1)][0] == neighbor[0]:
                    cat_hit += 0.00001
                    break
            tentative_gscore = gscore[current] + 1 + cat_hit
            if tentative_gscore < gscore[neighbor]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_gscore
                fscore[neighbor] = tentative_gscore + h(neighbor, goal, waypoints)
                open_set.add(neighbor)

    # print("NO PATH FOUND!!")
    return None


from heapq import *
def astarwpcath(maze,agent, start, goal, waypoints, h, upper,data, constraints=None):
    if (start[0], start[1], 0) in constraints:
        return None

    start_state = (start, 0, frozenset(waypoints))

    came_from = dict()
    gscore = defaultdict(constant_factory(inf))
    gscore[start_state] = 0
    fscore = defaultdict(constant_factory(inf))
    fscore[start_state] = h(start_state, goal, waypoints,data)

    open_set = []
    heappush(open_set, (fscore[start_state], start_state))
    close_set = set()

    while open_set:
        current = heappop(open_set)[1]
        # current = min_test(open_set, key=lambda x: fscore[x])
        if current[0] == goal and not current[2]:
            if not constraints or current[1] >= max(constraints, key=lambda x: x.time).time:
                return reconstruct_path(came_from, current)

        # open_set.remove(current)
        close_set.add(current)
        for neighbor in maze.reachable_from_with_waypoints(current, constraints=constraints):
            cat_hit = 0
            for path in upper.solution:
                if agent == path.agent:
                    continue
                if path[fast_min(neighbor[1], len(path) - 1)][0] == neighbor[0]:
                    cat_hit += 0.001
                    break
            tentative_gscore = gscore[current] + 1 + cat_hit
            if neighbor in close_set and tentative_gscore>gscore[neighbor]:
                continue
            if tentative_gscore < gscore[neighbor]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_gscore
                fscore[neighbor] = tentative_gscore + h(neighbor, goal, neighbor[2],data)*1.0000001
                # open_set.add(neighbor)
                heappush(open_set, (fscore[neighbor], neighbor))

    # print("NO PATH FOUND!!")
    return None


class PointConstraint:
    def __init__(self, agent, place, time):
        self.agent = agent
        self.place = place[0]
        if time:
            self.time = time
        else:
            self.time = place[1]

    def __eq__(self, other):
        if isinstance(other, PointConstraint):
            return self.agent == other.agent and self.place == other.place and self.time is other.time
        if isinstance(other, list) or isinstance(other, tuple):
            if len(other)!=3:
                return False
            return self.place[0] == other[0] and self.place[1] == other[1] and self.time == other[2]
        return False

    def __hash__(self):
        return hash(hash(self.agent.name)+hash(self.place)+hash(self.time))

class EdgeConstraint:
    def __init__(self, agent, place1,place2, time):
        self.agent = agent
        self.place1 = place1[0]
        self.place2 = place2[0]
        self.time = time

    def __eq__(self, other):
        if isinstance(other, EdgeConstraint):
            return self.agent == other.agent and self.place1 == other.place1 and self.place2 == other.place2 and self.time is other.time
        if isinstance(other, list) or isinstance(other, tuple):
            if len(other)!=5:
                return False
            return self.place1[0] == other[0] and self.place1[1] == other[1] and self.place2[0] == other[2] and self.place2[1] == other[3] and self.time == other[4]
        return False

    def __hash__(self):
        return hash(hash(self.agent.name)+hash(self.place1)+hash(self.place2)+hash(self.time))


class SingleAgentCosntraints:
    def __init__(self, constraints):
        if constraints:
            self.constraints = constraints
        else:
            self.constraints = []

    def __contains__(self, item):
        return item in self.constraints

    def __iter__(self):
        for constraint in self.constraints:
            yield constraint

    def __getitem__(self, item):
        return self.constraints[item]

    def __bool__(self):
        return bool(self.constraints)

    @staticmethod
    def from_constraints(agent, constraints):
        return SingleAgentCosntraints([constraint for constraint in constraints if constraint.agent == agent])


class PointConflict:
    def __init__(self, agent_1, agent_2, place, time):
        self.agent_1 = agent_1
        self.agent_2 = agent_2
        self.place = place
        self.time = time


class EdgeConflict:
    def __init__(self, agent_1, agent_2, place_1, place_2, time):
        self.agent_1 = agent_1
        self.agent_2 = agent_2
        self.place_1 = place_1
        self.place_2 = place_2
        self.time = time


class SlideConflict:
    def __init__(self, agent_1, agent_2, place, time):
        self.agent_1 = agent_1
        self.agent_2 = agent_2
        self.place = place
        self.time = time


class Node:
    def __init__(self, constraints=None, solution=None, cost=None,h=0,agents=[]):
        if constraints:
            self.constraints = constraints
        else:
            self.constraints = []
        self.solution = solution
        self.cost = cost
        self.h = h
        self.cg = GD(agents)

    def print_solution(self):
        print(self.solution)


class Path:
    def __init__(self, agent, path=None):
        self.agent = agent
        if path:
            self.path = path
        else:
            self.path = []

    def __len__(self):
        return len(self.path)

    def __str__(self):
        return f"<Agent: {self.agent}, Path: {self.path}"

    def __getitem__(self, item):
        return self.path[item]

    def dup(self):
        return Path(self.agent,deepcopy(self.path))


class Solution:
    def __init__(self, paths):
        self.paths = paths

    def __iter__(self):
        for path in self.paths:
            yield path

    def __getitem__(self, item):
        if isinstance(item,Agent):
            for path in self.paths:
                if path.agent == item:
                    return path

    def __setitem__(self, key, value):
        if isinstance(key,Agent):
            for path in range(len(self.paths)):
                if self.paths[path].agent == key:
                    self.paths[path]=value
                    return

    def dup(self):
        return Solution([path.dup() for path in self.paths])


    def sum_of_individual_costs(self):
        return sum(len(path) for path in self.paths)

    def max_of_individual_costs(self):
        return max(len(path) for path in self.paths)

    def find_worst_conflict(self,maze,data,const,mem=dict()):
        confs = self.find_conflict(list_all=True)
        if not confs:
            return None
        md = dict()
        for p in self.paths:
            a = p.agent
            l = len(p)

            t = MDD.construct(maze,a.start,a.waypoints,a.goal,l,data,const).g
            md[a.name] = t

        semi_cardinal = None
        for c in confs:
            s = 0
            if isinstance(c, PointConflict):
                if len(md[c.agent_1.name][min(c.time,len(md[c.agent_1.name])-1)])<=1:
                    s+=1
                if len(md[c.agent_2.name][min(c.time,len(md[c.agent_2.name])-1)])<=1:
                    s+=1
            elif isinstance(c, EdgeConflict):
                if len(md[c.agent_1.name][min(c.time+1,len(md[c.agent_1.name])-1)])<=1:
                    s+=1
                if len(md[c.agent_2.name][min(c.time+1,len(md[c.agent_2.name])-1)])<=1:
                    s+=1
            if s == 2:
                return (c,s)
            if s == 1 and not semi_cardinal:
                semi_cardinal = c
        if semi_cardinal:
            return (semi_cardinal,1)
        return (confs[0],0)

    def find_conflict(self, slide=False,list_all=False):
        longest_path_length = self.max_of_individual_costs()
        lst = []
        for t in range(longest_path_length):
            for a1 in range(len(self.paths)):
                for a2 in range(a1):
                    # if len(self.paths[a1]) > t and len(self.paths[a2]) > t:
                    if self.paths[a1][min(t, len(self.paths[a1]) - 1)][0] == \
                            self.paths[a2][min(t, len(self.paths[a2]) - 1)][0]:
                        conf = PointConflict(self.paths[a1].agent, self.paths[a2].agent,
                                             self.paths[a1][min(t, len(self.paths[a1]) - 1)], t)
                        if list_all:
                            lst.append(conf)
                        else:
                            return conf
                    if len(self.paths[a1]) > t + 1 and len(self.paths[a2]) > t + 1:
                        if self.paths[a1][t][0] == self.paths[a2][t + 1][0] and self.paths[a1][t + 1][0] == \
                                self.paths[a2][t][0]:
                            conf = EdgeConflict(self.paths[a1].agent, self.paths[a2].agent, self.paths[a1][t],
                                                self.paths[a2][t], t)
                            if list_all:
                                lst.append(conf)
                            else:
                                return conf
                    if slide:
                        if len(self.paths[a1]) > t + 1 and len(self.paths[a2]) > t + 1:
                            if (abs(self.paths[a1][t][0][0] - self.paths[a1][t + 1][0][0]) or abs(
                                    self.paths[a1][t][0][1] - self.paths[a1][t + 1][0][1])) and (
                                    abs(self.paths[a1][t][0][0] - self.paths[a1][t + 1][0][0]) == abs(
                                    self.paths[a2][t][1] - self.paths[a2][t + 1][0][1]) or abs(
                                    self.paths[a1][t][0][1] - self.paths[a1][t + 1][0][1]) == abs(
                                    self.paths[a2][t][0][0] - self.paths[a2][t + 1][0][0])):
                                if self.paths[a1][t + 1][:1] == self.paths[a2][t][:1]:
                                    return SlideConflict(self.paths[a1].agent, self.paths[a2].agent, self.paths[a2][t],
                                                         t)
                                if self.paths[a2][t + 1][:1] == self.paths[a1][t][:1]:
                                    return SlideConflict(self.paths[a2].agent, self.paths[a1].agent, self.paths[a1][t],
                                                         t)
        if list_all:
            return lst
        else:
            return None

    def __str__(self):
        return "<Solution:\n" + "\n".join(str(path) for path in self.paths)


def solve(maze, constraints, upper=None,data=None):
    if not upper:
        upper = Node()
        upper.solution = Solution([])
    paths = []
    for agent in maze.agents:
        # a_path = astarwp(maze, agent.start, agent.goal, agent.waypoints, waypointheuristic,
        #                 SingleAgentCosntraints.from_constraints(agent, constraints))
        # a_path = astarwpcat(maze, agent, agent.start, agent.goal, agent.waypoints, waypointheuristic,upper,
        #                  SingleAgentCosntraints.from_constraints(agent, constraints))
        a_path = astarwpcath(maze, agent, agent.start, agent.goal, agent.waypoints, perfect_heuristic, upper,data,
                            SingleAgentCosntraints.from_constraints(agent, constraints))
        if a_path is None:
            # print("No Path with constraints")
            return None
        paths.append(Path(agent, a_path))
    return Solution(paths)

def replan(maze, constraints, agent, upper,data=None):
    # a_path = astarwpcat(maze, agent, agent.start, agent.goal, agent.waypoints, waypointheuristic,upper,
    #                  SingleAgentCosntraints.from_constraints(agent, constraints))
    # a_path = astarwp(maze, agent.start, agent.goal, agent.waypoints, waypointheuristic,
    #                     SingleAgentCosntraints.from_constraints(agent, constraints))
    a_path = astarwpcath(maze, agent, agent.start, agent.goal, agent.waypoints, perfect_heuristic, upper, data,
                         SingleAgentCosntraints.from_constraints(agent, constraints))
    if a_path is None:
        # print("No Path with constraints")
        return None
    new_solution = upper.solution.dup()
    new_solution[agent] = Path(agent,a_path)
    return new_solution

def flood_dists(maze, pos):
    q = [pos]
    discovered = {pos}
    dists = {pos: 0}
    while q:
        v = q.pop(0)
        for w in maze.reachable_from_pos(v):
            if not w in discovered:
                discovered.add(w)
                dists[w]=dists[v]+1
                q.append(w)
    return dists


def build_cg(maze, heuristic_data, solution, constraints,mem=dict()):
    confs = solution.find_conflict(list_all=True)
    if not confs:
        return set()

    edg = set()

    md = dict()
    for p1 in solution.paths:
        for p2 in solution.paths:
            if p1!=p2:

                a1 = p1.agent
                a2 = p2.agent
                l1 = len(p1)
                t1 = MDD.construct(maze, a1.start, a1.waypoints, a1.goal, l1, heuristic_data, constraints)
                l2 = len(p2)
                t2 = MDD.construct(maze, a2.start, a2.waypoints, a2.goal, l2, heuristic_data, constraints)
                c = MDD.merge(t1,t2)
                if c:
                    edg.add((p1.agent,p2.agent))

    return edg



def CBS(maze,pc=True):
    dist_data = dict()
    for agent in maze.agents:
        dist_data[agent.goal] = flood_dists(maze,agent.goal)
        for waypoint in agent.waypoints:
            dist_data[waypoint] = flood_dists(maze,waypoint)

    # print("p1")

    compl_dists = dict()
    # for agent in maze.agents:
    #     open_waypoints = powerset(agent.waypoints)
    #     for waypoint_combi in open_waypoints:
    #         print(waypoint_combi)
    #         if not waypoint_combi:
    #             continue
    #         for start_point in waypoint_combi:
    #             rest = (point for point in waypoint_combi if point != start_point)
    #             best = inf
    #             for perm in permutations(rest):
    #                 d = 0
    #                 cp = start_point
    #                 for tp in perm:
    #                     d+=dist_data[tp][cp]
    #                     cp = tp
    #                 d+=dist_data[agent.goal][cp]
    #                 best = fast_min(best,d)
    #             compl_dists[(start_point,frozenset(waypoint_combi))] = best

    heuristic_data = {"direct":dist_data,"wp":compl_dists}

    # print("go")

    r = Node(agents=list(maze.agents))
    r.solution = solve(maze, r.constraints,data=heuristic_data)
    r.cost = r.solution.sum_of_individual_costs()
    # return r.solution

    # r.cg.edges = build_cg(maze,heuristic_data,r.solution,r.constraints)

    open_set = {r}
    while open_set:
        p = min(open_set, key=lambda x: x.cost+x.h)
        open_set.remove(p)
        conflict = p.solution.find_conflict(list_all=True)
        print(p.cost,len(conflict),len(p.constraints))
        if pc:
            conflict = p.solution.find_worst_conflict(maze, heuristic_data, p.constraints)
        else:
            conflict = p.solution.find_conflict()

        if conflict is None:
            # print(p.cost)
            return p.solution
        if pc:
            conflict = conflict[0]
        if isinstance(conflict, PointConflict):
            a = Node()
            a.constraints = p.constraints + [PointConstraint(conflict.agent_1, conflict.place, conflict.time)]
            a.solution = replan(maze, a.constraints,conflict.agent_1,p,data=heuristic_data)
            if a.solution:
                a.cost = a.solution.sum_of_individual_costs()
                if a.cost == p.cost and len(a.solution.find_conflict(list_all=True)) < len(
                        p.solution.find_conflict(list_all=True)):
                    open_set.add(a)
                    continue

            b = Node()
            b.constraints = p.constraints + [PointConstraint(conflict.agent_2, conflict.place, conflict.time)]
            b.solution = replan(maze, b.constraints,conflict.agent_2,p,data=heuristic_data)
            if b.solution:
                b.cost = b.solution.sum_of_individual_costs()
                if b.cost == p.cost and len(b.solution.find_conflict(list_all=True)) < len(
                        p.solution.find_conflict(list_all=True)):
                    open_set.add(b)
                    continue
                open_set.add(b)
            if a.solution:
                open_set.add(a)

        elif isinstance(conflict, EdgeConflict):
            a = Node()
            a.constraints = p.constraints + [EdgeConstraint(conflict.agent_1,conflict.place_1, conflict.place_2, conflict.time + 1)]
            a.solution = replan(maze, a.constraints,conflict.agent_1,p,data=heuristic_data)
            if a.solution:
                a.cost = a.solution.sum_of_individual_costs()
                if a.cost == p.cost and len(a.solution.find_conflict(list_all=True)) < len(
                        p.solution.find_conflict(list_all=True)):
                    open_set.add(a)
                    continue

            b = Node()
            b.constraints = p.constraints + [EdgeConstraint(conflict.agent_2,conflict.place_2, conflict.place_1, conflict.time + 1)]
            b.solution = replan(maze, b.constraints,conflict.agent_2,p,data=heuristic_data)
            if b.solution:
                b.cost = b.solution.sum_of_individual_costs()
                if b.cost == p.cost and len(b.solution.find_conflict(list_all=True)) < len(
                        p.solution.find_conflict(list_all=True)):
                    open_set.add(b)
                    continue
                open_set.add(b)
            if a.solution:
                open_set.add(a)

        elif isinstance(conflict, SlideConflict):
            a = Node()
            a.constraints = p.constraints + [PointConstraint(conflict.agent_1, conflict.place, conflict.time + 1)]
            a.solution = solve(maze, a.constraints,p)
            if a.solution:
                a.cost = a.solution.sum_of_individual_costs()
                open_set.add(a)

            b = Node()
            b.constraints = p.constraints + [PointConstraint(conflict.agent_2, conflict.place, conflict.time)]
            b.solution = solve(maze, b.constraints,p)
            if b.solution:
                b.cost = b.solution.sum_of_individual_costs()
                open_set.add(b)
