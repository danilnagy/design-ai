import Rhino.Geometry as rh

# set up geometry pipeline GH component for the boundary and add new varible to GH ptyhon
# component with its type hint set to "polyline". draw a randown polyline as "boundary"(b)


class Agent:

    # add boundry attriibute to agent

    def __init__(self, pt, r, b):

        self.cp = pt
        self.radius = r
        self.neighbors = []
        self.boundary = b

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

    # add new method for colliding with given boundary and clustering toward its center
    def collideboundary(self, other, alpha):

        # get overlapping distance
        d = self.cp.DistanceTo(self.boundary.ClosestPoint(self.cp))

        amount = 0

        # check for overlapping
        if d < self.radius:

            pt_2 = self.boundary.CenterPoint()
            pt_1 = self.cp

            # get vector direction from self to boundary center point
            v = pt_1 - pt_2

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= self.radius - d
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

    # add new method for colliding with given boundary and clustering toward its center
    def clusterboundary(self, other, alpha):

        # get the distance between the agent and boundary center and the the its length that
        # falls within the boundary
        dCenterToSelf = self.cp.DistanceTo(self.boundary.CenterPoint())
        dCenterToBoundary = self.boundary.CenterPoint().DistanceTo(
            self.boundary.ClosestPoint(self.cp))

        amount = 0

        # compare and check if agent is outside the boundary
        if dCenterToSelf > dCenterToBoundary:

            pt_2 = self.boundary.CenterPoint()
            pt_1 = self.cp

            # get vector direction from self to boundary center point
            v = pt_1 - pt_2

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= dCenterToSelf - dCenterToBoundary + 2 * self.radius
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v *= (alpha)

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

    def get_circle(self):
        return rh.Circle(self.cp, self.radius)


def run(pts, radii, max_iters, alpha, adjacencies, b):

    print(adjacencies)

    agents = []

    for i, pt in enumerate(pts):
        my_agent = Agent(pt, radii[i], b)
        agents.append(my_agent)

    # for each agent in the list, add the previous agent as its neighbor
    for i in range(len(agents)):
        agents[i].add_neighbor(agents[i-1])

    for i in range(max_iters):

        total_amount = 0

        for j, agent_1 in enumerate(agents):

            # cluster to all agent's neighbors
            for agent_2 in agent_1.neighbors:
                total_amount += agent_1.cluster(agent_2, alpha)

            # collide with all agents after agent in list
            for agent_2 in agents[j+1:]:
                # add extra multiplier to decrease effect of cluster
                total_amount += agent_1.collide(agent_2, alpha/20)

        if total_amount < .01:
            break

        for j, agent_1 in enumerate(agents):

            # all agent's neighbors cluster to boundary center point
            for agent_2 in agent_1.neighbors:
                total_amount += agent_1.clusterboundary(agent_2, alpha)

            # collide with boundary after agent in list
            for agent_2 in agents[j+1:]:
                # add extra multiplier to decrease effect of cluster
                total_amount += agent_1.collideboundary(agent_2, alpha/20)

        if total_amount < .01:
            break

    iters = i

    print("process ran for {} iterations".format(i))

    circles = []

    for agent in agents:
        circles.append(agent.get_circle())

    return circles, iters
