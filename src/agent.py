class Agent:
    def __init__(self, name, pos=None, start=None, goal=None, waypoints=None):
        self.name = name
        self.pos = pos
        self.start = start
        self.goal = goal
        if waypoints:
            self.waypoints = waypoints
        else:
            self.waypoints = []

    def add_waypoint(self, point):
        self.waypoints.append(point)

    def set_start(self, point):
        self.start = point[:]
        self.pos = point[:]

    def __str__(self):
        txt = f"<Agent {self.name}\n" \
            f"\tpos: {self.pos}\n" \
            f"\tstart: {self.start}\n" \
            f"\tgoal: {self.goal}\n" \
            f"\twaypoints:\n"
        for point in self.waypoints:
            txt += f"\t{point}\n"
        txt += ">"
        return txt

    def __eq__(self, other):
        if not isinstance(other,Agent):
            return False
        return self.name == other.name
