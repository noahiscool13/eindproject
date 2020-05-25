class AgentPool:
    def __init__(self):
        self.agents = {}

    def add(self, agent):
        self.agents[agent.name] = agent

    def get(self, agent):
        return self.agents[agent]

    def __str__(self):
        txt = "Pool:\n" + "\n".join(str(agent) for agent in self.agents.values()) + "\n"
        return txt

    def __iter__(self):
        for agent in self.agents.values():
            yield agent

    def __getitem__(self, item):
        return list(self.agents.values())[item]

    def print_names(self):
        print(list(self.agents.keys()))
