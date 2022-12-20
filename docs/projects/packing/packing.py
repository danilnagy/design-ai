import Rhino.Geometry as rh
import math

# connect "names" from json file to gh python component as a list
# using gene pool, add new list with values range from 0.5 tp 2.0. values in this list represent width
# to height ratios for rectangular spaces


class Agent:

    # define new rectangles with area, width, and height
    # add room name and adjacency attributes to agent
    def __init__(self, pt, a, adj, ratio, name):

        self.cp = pt
        self.area = a
        self.neighbors = []
        self.ratio = ratio
        self.ZVector = rh.Vector3d(0, 0, 1)
        self.plane = rh.Plane(pt, self.ZVector)
        self.width = ratio * math.sqrt(a)
        self.height = self.area / self.width
        self.rect = rh.Rectangle3d(self.plane, rh.Point3d(self.cp.X + 0.5 * self.width,
                                                          self.cp.Y + 0.5 * self.height, 0), rh.Point3d(self.cp.X - 0.5 * self.width,
                                                                                                        self.cp.Y - 0.5 * self.height, 0))
        self.adjacency = adj
        self.name = name

    # method for adding another instance to a list of neighbors

    def add_neighbor(self, other):
        self.neighbors.append(other)

    # method for checking distance to other room object and moving apart if they are overlapping
    def collide(self, other, alpha):

        d = self.cp.DistanceTo(other.cp)

        other.rect = rh.Rectangle3d(self.plane, rh.Point3d(other.cp.X + 0.5 * other.width,
                                                           other.cp.Y + 0.5 * other.height, 0), rh.Point3d(other.cp.X - 0.5 * other.width,
                                                                                                           other.cp.Y - 0.5 * other.height, 0))

        # find shortest distance between two rectangles while they are just touching each other

        pt_intersectOther = rh.PolylineCurve([self.cp, other.cp]).ClosestPoints(
            other.rect.ToNurbsCurve())[1]

        pt_intersectSelf = rh.PolylineCurve([self.cp, other.cp]).ClosestPoints(
            self.rect.ToNurbsCurve())[1]

        selfDistToIntersectBoundaryPoint = self.cp.DistanceTo(
            pt_intersectSelf)
        otherDistToIntersectBoundaryPoint = other.cp.DistanceTo(
            pt_intersectOther)

        amount = 0

        # update collide logic based on shortest distance between two rectangles

        if d < selfDistToIntersectBoundaryPoint + otherDistToIntersectBoundaryPoint:

            pt_2 = other.cp
            pt_1 = self.cp

            # get vector from self to other
            v = pt_2 - pt_1

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= (selfDistToIntersectBoundaryPoint +
                  otherDistToIntersectBoundaryPoint - d) / 2
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

        other.rect = rh.Rectangle3d(self.plane, rh.Point3d(other.cp.X + 0.5 * other.width,
                                                           other.cp.Y + 0.5 * other.height, 0), rh.Point3d(other.cp.X - 0.5 * other.width,
                                                                                                           other.cp.Y - 0.5 * other.height, 0))

        # find shortest distance between two rectangles while they are just touching each other

        pt_intersectOther = rh.PolylineCurve([self.cp, other.cp]).ClosestPoints(
            other.rect.ToNurbsCurve())[1]

        pt_intersectSelf = rh.PolylineCurve([self.cp, other.cp]).ClosestPoints(
            self.rect.ToNurbsCurve())[1]

        selfDistToIntersectBoundaryPoint = self.cp.DistanceTo(
            pt_intersectSelf)
        otherDistToIntersectBoundaryPoint = other.cp.DistanceTo(
            pt_intersectOther)

        amount = 0

        # update cluster logic based on shortest distance between two rectangles

        if d > selfDistToIntersectBoundaryPoint + otherDistToIntersectBoundaryPoint:

            pt_2 = other.cp
            pt_1 = self.cp

            # get vector from self to other
            v = pt_2 - pt_1

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= (d - (selfDistToIntersectBoundaryPoint +
                  otherDistToIntersectBoundaryPoint)) / 2
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

# get new rectangles using two farest points

    def get_rect(self):
        a = rh.Point3d(self.cp.X + 0.5 * self.width,
                       self.cp.Y + 0.5 * self.height, 0)
        b = rh.Point3d(self.cp.X - 0.5 * self.width,
                       self.cp.Y - 0.5 * self.height, 0)
        return rh.Rectangle3d(self.plane, a, b)


def run(pts, a, max_iters, alpha, adjacencies, ratio, names):

    print(adjacencies)
    print(ratio)

    agents = []

    for i, pt in enumerate(pts):
        my_agent = Agent(pt, a[i], adjacencies[names[i]], ratio[i], names[i])
        agents.append(my_agent)

    # # for each agent in the list, add agent that fullfills adjacency requirment as its new neighbor
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
                total_amount += agent_1.cluster(agent_2, alpha)

            # collide with all agents after agent in list
            for agent_2 in agents[j+1:]:
                # add extra multiplier to decrease effect of cluster
                total_amount += agent_1.collide(agent_2, alpha/5)

        if total_amount < .01:
            break

    iters = i

    print("process ran for {} iterations".format(i))

    rectangles = []

    for agent in agents:
        rectangles.append(agent.get_rect())

    return rectangles, iters
