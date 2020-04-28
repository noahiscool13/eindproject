import json
from time import time

import requests

from src.CBS import CBS
from src.agent import Agent
from src.maze import Maze
from src.vizualizer import create_gif

headers = {
           'X-API-Token': '13'
           }

data = {
	"algorithm": "CBS",
	"version": "0"
}
# r = requests.post("https://mapfw.nl/api/benchmarks/2/problems",headers=headers,json=data)
r = requests.post("http://127.0.0.1:5000/api/benchmarks/5/problems",headers=headers,json=data)

n = r.json()
problem = json.loads(r.json()["problems"][0]["problem"])
at_id = r.json()["attempt"]
# print(problem)

n_agents = len(problem["starts"])
agents = [Agent(f"[{x*347%256},{x*9231%256}]",tuple(problem["starts"][x]),tuple(problem["starts"][x]),tuple(problem["goals"][x]),set(tuple(n) for n in problem["waypoints"][x])) for x in range(n_agents)]
maze = Maze(problem["grid"],agents)


t = time()
paths = CBS(maze)
t = time()-t
create_gif("test3.gif", maze, paths, 20)
ans = {
	"solutions": [
		{
			"problem": r.json()["problems"][0]["id"],
			"time": round(t*1000),
			"solution": [[y[0] for y in x.path] for x in paths]
		}
	]
}

print(ans)

# r = requests.post(f"https://mapfw.nl/api/attempts/{at_id}/solutions",headers=headers,json=ans)
r = requests.post(f"http://127.0.0.1:5000/api/attempts/{at_id}/solutions",headers=headers,json=ans)

print(r.content)