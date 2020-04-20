from collections import defaultdict

from math import inf


def constant_factory(value):
    return lambda: value


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]


def manhatan(pos, goal):
    return abs(pos[0][0] - goal[0]) + abs(pos[0][1] - goal[1])

def waypointheuristic(pos,goal,waypoints):
    if not waypoints:
        return manhatan(pos,goal)
    furtherst = max(waypoints,key=lambda waypoint:manhatan(pos,waypoint))
    return manhatan(pos,furtherst)+len(waypoints)-1+manhatan((furtherst,0),goal)


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

    print("NO PATH FOUND!!")
    return None


def astarwp(maze, start, goal,waypoints, h, constraints=None):
    start_state = (start, 0,frozenset(waypoints))
    open_set = {start_state}
    came_from = dict()
    gscore = defaultdict(constant_factory(inf))
    gscore[start_state] = 0
    fscore = defaultdict(constant_factory(inf))
    fscore[start_state] = h(start_state, goal,waypoints)

    while open_set:
        current = min(open_set, key=lambda x: fscore[x])
        if current[0] == goal and not current[2]:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        for neighbor in maze.reachable_from_with_waypoints(current, constraints=constraints):
            tentative_gscore = gscore[current] + 1
            if tentative_gscore < gscore[neighbor]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_gscore
                fscore[neighbor] = tentative_gscore + h(neighbor, goal,waypoints)
                open_set.add(neighbor)

    print("NO PATH FOUND!!")
    return None


class Constraint:
    def __init__(self, agent, place, time):
        self.agent = agent
        self.place = place[0]
        if time:
            self.time = time
        else:
            self.time = place[1]

    def __eq__(self, other):
        if isinstance(other, Constraint):
            return self.agent == other.agent and self.place == other.place and self.time is other.time
        if isinstance(other, list) or isinstance(other, tuple):
            return self.place[0] == other[0] and self.place[1] == other[1] and self.time == other[2]
        return False


class SingleAgentCosntraints:
    def __init__(self, constraints):
        if constraints:
            self.constraints = constraints
        else:
            self.constraints = []

    def __contains__(self, item):
        return item in self.constraints

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


class Node:
    def __init__(self, constraints=None, solution=None, cost=None):
        if constraints:
            self.constraints = constraints
        else:
            self.constraints = []
        self.solution = solution
        self.cost = cost

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


class Solution:
    def __init__(self, paths):
        self.paths = paths

    def sum_of_individual_costs(self):
        return sum(len(path) for path in self.paths)

    def max_of_individual_costs(self):
        return max(len(path) for path in self.paths)

    def find_conflict(self):
        longest_path_length = self.max_of_individual_costs()
        for t in range(longest_path_length):
            for a1 in range(len(self.paths)):
                for a2 in range(a1):
                    if len(self.paths[a1]) > t and len(self.paths[a2]) > t:
                        if self.paths[a1][t][:2] == self.paths[a2][t][:2]:
                            return PointConflict(self.paths[a1].agent, self.paths[a2].agent, self.paths[a1][t], t)
                    if len(self.paths[a1]) > t + 1 and len(self.paths[a2]) > t + 1:
                        if self.paths[a1][t][0] == self.paths[a2][t + 1][0] and self.paths[a1][t + 1][0] == \
                                self.paths[a2][t][0]:
                            return EdgeConflict(self.paths[a1].agent, self.paths[a2].agent, self.paths[a1][t],
                                                self.paths[a2][t], t)
        return None

    def __str__(self):
        return "<Solution:\n" + "\n".join(str(path) for path in self.paths)


def solve(maze, constraints):
    paths = []
    for agent in maze.agents:
        # a_path = astar(maze, agent.start, agent.goal, manhatan,
        #                SingleAgentCosntraints.from_constraints(agent, constraints))
        a_path = astarwp(maze, agent.start, agent.goal, agent.waypoints, waypointheuristic,
                       SingleAgentCosntraints.from_constraints(agent, constraints))
        if a_path is None:
            print("No Path with constraints")
            return None
        paths.append(Path(agent, a_path))
    return Solution(paths)


def CBS(maze):
    r = Node()
    r.solution = solve(maze, r.constraints)
    r.cost = r.solution.sum_of_individual_costs()
    open_set = {r}
    while open_set:
        p = min(open_set, key=lambda x: x.cost)
        open_set.remove(p)
        conflict = p.solution.find_conflict()
        print(len(p.constraints))
        if conflict is None:
            return p.solution
        if isinstance(conflict, PointConflict):
            a = Node()
            a.constraints = p.constraints + [Constraint(conflict.agent_1, conflict.place, conflict.time)]
            a.solution = solve(maze, a.constraints)
            if a.solution:
                a.cost = a.solution.sum_of_individual_costs()
                open_set.add(a)

            b = Node()
            b.constraints = p.constraints + [Constraint(conflict.agent_2, conflict.place, conflict.time)]
            b.solution = solve(maze, b.constraints)
            if b.solution:
                b.cost = b.solution.sum_of_individual_costs()
                open_set.add(b)

        elif isinstance(conflict, EdgeConflict):
            a = Node()
            a.constraints = p.constraints + [Constraint(conflict.agent_1, conflict.place_2, conflict.time + 1)]
            a.solution = solve(maze, a.constraints)
            if a.solution:
                a.cost = a.solution.sum_of_individual_costs()
                open_set.add(a)

            b = Node()
            b.constraints = p.constraints + [Constraint(conflict.agent_2, conflict.place_1, conflict.time + 1)]
            b.solution = solve(maze, b.constraints)
            if b.solution:
                b.cost = b.solution.sum_of_individual_costs()
                open_set.add(b)
