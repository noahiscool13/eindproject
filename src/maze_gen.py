import json


class Problem:
    def __init__(self, maze, width, height, starts, goals, waypoints=()):
        self.grid = maze
        self.width = width
        self.height = height
        self.starts = starts
        self.goals = goals
        self.waypoints = waypoints

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_file(filename,scenario,num_agents=0):
        scen_file = open(filename,"r")
        lines = [line for line in scen_file.readlines() if line.startswith(str(scenario)+"\t")]
        starts = []
        goals = []
        for line in lines:
            line = line.split()
            starts.append([int(line[4]), int(line[5])])
            goals.append([int(line[6]), int(line[7])])
        if num_agents:
            starts = starts[:num_agents]
            goals = goals[:num_agents]
        map_file = open("maze-map/"+lines[0].split()[1],"r").readlines()
        height = map_file[1].split()[1]
        width = map_file[2].split()[1]
        maze = map_file[4:]
        maze = [[0 if x == "." else 1 for x in row] for row in maze]

        return Problem(maze,width,height,starts,goals)




# p = Problem([[1,0],[0,0]],[(1,0)],[(0,1)],[(1,1)])
#


p = Problem.from_file("maze-scen/maze512-1-0.map.scen",5,2)

print(p.to_json())