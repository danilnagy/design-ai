import Rhino.Geometry as rh


class Agent:
    # add name and adjacency fileds to class, also add names and adjacencies input in ghpython components
    def __init__(self, pt, r, id, adjcs):

        self.cp = pt
        self.radius = r
        self.name = id
        self.adjacency = adjcs
        self.neighbors = []

    # method for adding another instance to a list of neighbors
    def add_neighbor(self, other):
        self.neighbors.append(other)

    # method for checking distance to other room object and moving apart if they are overlapping
    def collide(self, other, alpha):

        d = self.cp.DistanceTo(other.cp)

        amount = 0

        if d < self.radius + other.radius:

            pt_2 = other.cp
            pt_1 = self.cp

            # get vector from self to other
            v = pt_2 - pt_1

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= (self.radius + other.radius - d) / 2
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v *= alpha

            amount = v.Length

            # move other object
            t = rh.Transform.Translation(v)
            pt_2.Transform(t)

            # reverse vector and move self same amount
            # in opposite direction
            v.Reverse()
            t = rh.Transform.Translation(v)
            pt_1.Transform(t)

        return amount

    # method for checking distance to other instance and moving closer if they are not touching
    def cluster(self, other, alpha):

        d = self.cp.DistanceTo(other.cp)

        amount = 0

        if d > self.radius + other.radius:

            pt_2 = other.cp
            pt_1 = self.cp

            # get vector from self to other
            v = pt_2 - pt_1

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= (d - (self.radius + other.radius)) / 2
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v *= alpha

            amount = v.Length

            # move self
            t = rh.Transform.Translation(v)
            pt_1.Transform(t)

            # reverse vector and move other object same amount
            # in opposite direction
            v.Reverse()
            t = rh.Transform.Translation(v)
            pt_2.Transform(t)

        return amount

    def get_circle(self):
        return rh.Circle(self.cp, self.radius)


# add function signatures : names, adjacencies, also need to add these to ghython code to call this fucntion
def run(pts, radii, max_iters, alpha, adjacencies, names):
    # test if json data 'adjacencies' sucessfuly input
    print(adjacencies)
    # test if json data 'names' sucessfuly input
    print(names)

    agents = []

    for i, pt in enumerate(pts):
        print(names[i])
        # add names[i] and adjacencies[names[i]] to build my_agent
        my_agent = Agent(pt, radii[i], names[i], adjacencies[names[i]])
        agents.append(my_agent)
    # for each agent in the list, add the its all adjacency agents as its neighbor
    for i in range(len(agents)):
        for j in range(len(agents)):

            if agents[j].name in agents[i].adjacency:
                agents[i].add_neighbor(agents[j])
            else:
                continue

    for i in range(max_iters):

        total_amount = 0

        for j, agent_1 in enumerate(agents):

            # cluster to all agent's neighbors
            for agent_2 in agent_1.neighbors:
                total_amount += agent_1.cluster(agent_2, alpha/2)

            # collide with all agents after agent in list
            for agent_2 in agents[j+1:]:
                # add extra multiplier to decrease effect of cluster
                # adjust alpha/x to perfect ovelap ratio
                total_amount += agent_1.collide(agent_2, alpha/2)

        if total_amount < .01:
            break

    iters = i

    print("process ran for {} iterations".format(i))

    circles = []

    for agent in agents:
        circles.append(agent.get_circle())

    return circles, iters
