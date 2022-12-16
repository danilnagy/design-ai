import Rhino.Geometry as rh

class Agent:

    def __init__(self, pt, r, nam, adj, fl):

        self.cp = pt
        self.radius = r
        self.name = nam
        self.adjacency = adj
        self.floor = fl
        self.neighbors = []
        self.floorgroup = []

    # method for adding another instance to a list of neighbors
    def add_neighbor(self, other):

        self.neighbors.append(other)

    # method for adding all rooms on the same floor to a list of floor-mates
    def add_floorgroup(self, other):

        self.floorgroup.append(other)

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
        return rh.Circle(self.np, self.radius)

    def get_box(self):
        return rh.Circle(self.np, self.radius).BoundingBox
        

def run(pts, radii, names, adjacencies, floors, max_iters, alpha):

    agents = []

    for i, pt in enumerate(pts):
        my_agent = Agent(pt, radii[i], names[i], adjacencies[i], floors[i])
        agents.append(my_agent)

    # for each agent in the list, add any agent that has it within its adjacencies list as its neighbor
    for i in range(len(agents)):
        
        for j in range(len(agents)-1):

            for k in range(len(agents[j].floor)):
        
                if agents[j].name in agents[i].adjacency and agents[j].floor[k] in agents[i].floor:
                    agents[i].add_neighbor(agents[j])

                else:
                    continue

    for i in range(len(agents)):
        
        for j in range(len(agents)-1):

            for k in range(len(agents[j].floor)):
        
                if agents[j].floor[k] in agents[i].floor:
                    agents[i].add_floorgroup(agents[j])

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

                for i in range(len(agent_1.floor)):

                    if agent_1.floor[i] in agent_2.floor:

                        # add extra multiplier to decrease effect of cluster
                        total_amount += agent_2.collide(agent_1, alpha/5)

        if total_amount < .01:
            break

    iters = i

    # print("process ran for {} iterations".format(i))
    
    circles = []
    new_points = []
    new_names = []
    new_radii = []

    for agent in agents:

        for flr in agent.floor:

            pt_o = rh.Point3d(agent.cp)
            pt_1 = rh.Point3d(0,0,0)
            pt_2 = rh.Point3d(0,0,1)
            v = pt_2 - pt_1
            v *= ((flr * 20)-10)
            t = rh.Transform.Translation(v)
            pt_o.Transform(t)
            agent.np = pt_o

            new_points.append(pt_o)
            new_names.append(agent.name)
            new_radii.append(agent.radius)

            circles.append(agent.get_circle())

    stairs_base = []
    stairs_length = []
    stairs_radii = []

    for agent in agents:

        if len(agent.floor) > 1:

            pt_b = rh.Point3d(agent.cp)
            pt_1 = rh.Point3d(0,0,0)
            pt_2 = rh.Point3d(0,0,1)
            v = pt_2 - pt_1
            v *= ((agent.floor[0] * 20)-10)
            t = rh.Transform.Translation(v)
            pt_b.Transform(t)

            pt_t = rh.Point3d(agent.cp)
            pt_1 = rh.Point3d(0,0,0)
            pt_2 = rh.Point3d(0,0,1)
            v = pt_2 - pt_1
            v *= ((agent.floor[-1] * 20)-10)
            t = rh.Transform.Translation(v)
            pt_t.Transform(t)

            d = pt_b.DistanceTo(pt_t)

            stairs_base.append(pt_b)
            stairs_radii.append(agent.radius)
            stairs_length.append(d)

        else:
            continue

    
    flat_list = []

    for floor in floors:
        for item in floor:
            flat_list.append(item)

    box_1 = []
    box_2 = []
    box_3 = []

    for floor in list(set(flat_list)):

        for agent in agents:
            
            if floor in agent.floor:

                box = agent.get_box()

                for agent_x in agent.floorgroup:

                    if floor in agent_x.floor:
                
                        box = rh.BoundingBox.Union(box,agent_x.get_box())

                    else:
                        continue

        corners = rh.BoundingBox.GetCorners(box)
        box_1.append(corners[0])
        box_2.append(corners[2])
        box_3.append(corners[4])


    return circles, box_1, box_2, box_3, new_points, new_names, new_radii, stairs_base, stairs_length, stairs_radii, iters
