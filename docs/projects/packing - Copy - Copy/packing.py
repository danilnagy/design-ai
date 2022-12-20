import Rhino.Geometry as rh


class Agent:

    def __init__(self, pt, r):

        self.cp = pt
        self.width = r
        self.neighbors = []

    # method for adding another instance to a list of neighbors
    def add_neighbor(self, other):
        self.neighbors.append(other)

    # method for checking distance to other room object and moving apart if they are overlapping
    def collide(self, other, alpha):

        d_x = abs((pt_1.X - pt_2.X)/2)
        d_y = abs((pt_1.Y - pt_2.Y)/2)

        # d = self.cp.DistanceTo(other.cp)

        amount = 0

        if d_x < self.width + other.width:

            pt_2 = other.cp
            pt_1 = self.cp

            # get vector from self to other
            v = pt_2 - pt_1

            d_x = abs((pt_1.X - pt_2.X)/2)
            d_y = abs((pt_1.Y - pt_2.Y)/2)

            # change vector magnitude to 1
            v_x = v.X.Unitize()
            v_y = v.Y.Unitize()

            v_x *= d_x
            v_y *= d_y

            # set magnitude to half the overlap distance
            # v *= (self.radius + other.radius - d) / 2
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v_x *= alpha
            v_y *= alpha

            amount = v_x.Length

            # move other object
            t_x = rh.Transform.Translation(v_x)
            pt_2.Transform(t_x)

            t_y = rh.Transform.Translation(v_y)
            pt_2.Transform(t_y)

            # reverse vector and move self same amount
            # in opposite direction
            v_x.Reverse()
            v_y.Reverse()
            t_x = rh.Transform.Translation(v_x)
            pt_1.Transform(t_x)

            t_x = rh.Transform.Translation(v_x)
            pt_1.Transform(t_x)

            t_y = rh.Transform.Translation(v_y)
            pt_1.Transform(t_y)

        return amount

    # method for checking distance to other instance and moving closer if they are not touching
    def cluster(self, other, alpha):

        d_x = abs((pt_1.X - pt_2.X)/2)
        d_y = abs((pt_1.Y - pt_2.Y)/2)

        # d = self.cp.DistanceTo(other.cp)

        amount = 0

        if d_x > self.width + other.width:

            pt_2 = other.cp
            pt_1 = self.cp

            # get vector from self to other
            v = pt_2 - pt_1

            d_x = abs((pt_1.X - pt_2.X)/2)
            d_y = abs((pt_1.Y - pt_2.Y)/2)

            v_x = v.X.Unitize()
            v_y = v.Y.Unitize()

            v_x *= d_x
            v_y *= d_y

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= (d - (self.radius + other.radius)) / 2
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v_x *= alpha
            v_y *= alpha

            amount = v_x.Length

            # move self
            t_x = rh.Transform.Translation(v_x)
            pt_2.Transform(t_x)

            t_y = rh.Transform.Translation(v_y)
            pt_2.Transform(t_y)

            # reverse vector and move other object same amount
            # in opposite direction
            v_x.Reverse()
            v_y.Reverse()
            t_x = rh.Transform.Translation(v_x)
            pt_1.Transform(t_x)

            t_x = rh.Transform.Translation(v_x)
            pt_1.Transform(t_x)

            t_y = rh.Transform.Translation(v_y)
            pt_1.Transform(t_y)
        return amount

    def get_rectangle(self):
        return rh.Circle(self.cp, self.width, self.width)


def run(pts, width, max_iters, alpha, adjacencies):

    print(adjacencies)

    agents = []

    for i, pt in enumerate(pts):
        my_agent = Agent(pt, width[i])
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
                total_amount += agent_1.collide(agent_2, alpha/5)

        if total_amount < .01:
            break

    iters = i

    print("process ran for {} iterations".format(i))

    Rectangles = []

    for agent in agents:
        Rectangles.append(agent.get_rectangle())

    return Rectangles, iters
