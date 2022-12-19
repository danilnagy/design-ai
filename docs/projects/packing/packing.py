import Rhino.Geometry as rh
# add rhinoscriptsyntax
import rhinoscriptsyntax as rs


class Agent:
    # add name and adjacency fileds to class, also add names and adjacencies input in ghpython component
    def __init__(self, pt, r, id, adjcs):

        self.cp = pt
        self.radius = r
        self.name = id
        self.adjacency = adjcs
        self.neighbors = []

    # method for adding another instance to a list of neighbors

    def add_neighbor(self, other):
        self.neighbors.append(other)

    # method for enticing the circle to boundry
    def entice(self, boundry, alpha):
        param = rs.CurveClosestPoint(boundry, self.cp)
        # print(param)
        closept = rs.EvaluateCurve(boundry, param)
        rs.AddPoint(closept)

        d = self.cp.DistanceTo(closept)

        pt_1 = closept
        pt_2 = self.cp
        # get vector from self to closept
        v = pt_2 - pt_1

        # change vector magnitude to 1
        v.Unitize()

        # print(d)

        # sotre the result of checking if the point inside the boundry, insde = 1, outside = 0, on = 2
        situation = rs.PointInPlanarClosedCurve(self.cp, boundry)
        # if point insde boundry
        if situation == "1":
            # if d > radius, push to point to boundry
            if d > self.radius:
                v *= -d*alpha
            # if d <= radisu, pull back point against boundry
            else:
                v *= d*alpha

        # if point outsde boundry, only push to point to boundry
        if situation == "0":
            v *= d*alpha

        # if point on boudry do nothing, because the situtation will change due to collide and cluster function

        # move other object
        t = rh.Transform.Translation(v)
        pt_2.Transform(t)

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
def run(pts, radii, names, adjacencies, max_iters, alpha, boundry):
    # test if json data 'adjacencies' sucessfuly input
    print(adjacencies)
    # test if json data 'names' sucessfuly input
    print(names)

    agents = []

    for i, pt in enumerate(pts):
        print(names[i])
        # add names[i] and adjacencies[names[i]] to build my_agent
        my_agent = Agent(pt, radii[i], names[i], adjacencies[names[i]],)
        agents.append(my_agent)

    boundr1 = boundry

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
            # entice to all agent's
            agent_1.entice(boundry, alpha/10)
            # cluster and entice to all agent's neighbors
            for agent_2 in agent_1.neighbors:
                # cluster to all agent's neighbors
                total_amount += agent_1.cluster(agent_2, alpha)
                # entice to all agent's neighbors
                agent_1.entice(boundry, alpha/10)

            # collide and entice with all agents after agent in list
            for agent_2 in agents[j+1:]:
                # add extra multiplier to decrease effect of cluster
                # adjust alpha/x to perfect ovelap ratio
                # collide with all agents after agent in list
                total_amount += agent_1.collide(agent_2, alpha)
                # entice with all agents after agent in list
                agent_1.entice(boundry, alpha/10)

        if total_amount < .01:
            break

    iters = i

    print("process ran for {} iterations".format(i))

    circles = []

    for agent in agents:
        circles.append(agent.get_circle())

    return circles, iters, boundr1
