# 3 - np2837

import Rhino.Geometry as rh

class Agent:
    def __init__(self, pt, r):
        self.cp = pt
        self.radius = r
        self.neighbors = []

    def add_neighbor(self, other):
        self.neighbors.append(other)

    def collide(self, other):

        d = self.cp.DistanceTo(other.cp)
        count = 0

        if d < self.radius + other.radius:
            pt_2 = other.cp
            pt_1 = self.cp

            v = pt_2 - pt_1
            v.Unitize()
            v *= (self.radius + other.radius - d) / 2
            v *= alpha

            t = rh.Transform.Translation(v)
            pt_2.Transform(t)
            v.Reverse()
            t = rh.Transform.Translation(v)
            pt_1.Transform(t)

    def cluster(self, other):

        d = other.cp.DistanceTo(self.cp)

        if d > self.radius + other.radius:
            pt_2 = self.cp
            pt_1 = other.cp

        pass
            v = pt_2 - pt_1
            v.Unitize()
            v *= (self.radius + other.radius) / 2
            v *= beta

            t = rh.Transform.Translation(v)
            pt_2.Transform(t)

    def get_circle(self):
        return rh.Circle(self.cp, self.radius)

agents = []

for pt in pts:
    my_agent = Agent(pt, radius)
    agents.append(my_agent)

# for each agent in the list, add the previous agent as its neighbor
# found difficuly here
for i in range(len(agents)):
    agents[i].add_neighbor(agents[i-1])

for i in range(max_iters):
    
    x = 0
    
    for j,agent_1 in enumerate(agents):

        # cluster to all agent's neighbors
        for agent_2 in agent_1.neighbors:
            agent_1.cluster(agent_2)

            totlcount = x + agent_1.cluster(agent_2) 

        # collide with all agents after agent in list
        for agent_2 in agents[j+1:]:
            agent_1.collide(agent_2)

            x = x + agent_1.collide(agent_2)

circles = []

for agent in agents:
    circles.append(agent.get_circle())
