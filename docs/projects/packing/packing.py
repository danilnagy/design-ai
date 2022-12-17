# NAME: QING HOU
# UNI: qh2195

import Rhino.Geometry as rh
import random
import math

class Agent:

    def __init__(self, pt, r):
        self.cp = pt
        self.area = r*r
        self.neighbors = []
        self.normalVector = rh.Vector3d(0,0,1)
        self.plane = rh.Plane(pt, self.normalVector)
        
        # Define a random weight-height ratio, to make a rectangle
        width_height_ratio = random.uniform(0.3, 0.6)
        # The width of the rectangle is defined as the r*width_height ratio
        self.width = r*width_height_ratio*2
        # Because it is rectangle, therefore the height is defined as area/width
        self.height = self.area/self.width
        # Redefined the radius
        self.radius = math.sqrt(self.width*self.width/4 + self.height*self.height/4)

    # method for adding another instance to a list of neighbors
    def add_neighbor(self, other):
        self.neighbors.append(other)

    # method for checking distance to other room object and moving apart if they are overlapping
    def collide(self, other, alpha):
        # for collide method, it should be based on Manhattan distance instead of Euclidean distance
        
        d_x = abs(self.cp.X - other.cp.X)
        d_y = abs(self.cp.Y - other.cp.Y)
        amount = 0

        # Check the amount of distance on x-axis
        if d_x < self.width/2.0 + other.width/2.0:
            pt_2 = other.cp
            pt_1 = self.cp

            # Get the center point's X-coordinates
            pt_2_x = rh.Point3d(other.cp.X, 0, 0)
            pt_1_x = rh.Point3d(self.cp.X, 0, 0)


            # get vector from self to other (on x_axis)
            v = pt_2_x - pt_1_x

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance (x_axis)
            v *= (self.width/2 + other.width/2 - d_x)
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v *= alpha        
            # amount of movement = sqrt(vx.length^2 + vy.length^2)
            amount = v.Length*v.Length

            # move other object
            t = rh.Transform.Translation(v)
            pt_2.Transform(t)

            # reverse vector and move self same amount
            # in opposite direction
            v.Reverse()
            t = rh.Transform.Translation(v)
            pt_1.Transform(t)

        # Check the amount of distance on y-axis
        if d_y < self.height/2.0 + other.height/2.0:
            pt_2 = other.cp
            pt_1 = self.cp

            # Get the center point's y-coordinates
            pt_2_y = rh.Point3d(0,other.cp.Y, 0)
            pt_1_y = rh.Point3d(0,self.cp.Y, 0)


            # get vector from self to other (y_axis)
            v = pt_2_y - pt_1_y

            # change vector magnitude to 1
            v.Unitize()

            # set magnitude to half the overlap distance
            v *= (self.height/2 + other.height/2 - d_y)
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v *= alpha

            # amount of movement = sqrt(vx.length^2 + vy.length^2)
            amount += v.Length*v.Length

            # move other object
            t = rh.Transform.Translation(v)
            pt_2.Transform(t)

            # reverse vector and move self same amount
            # in opposite direction
            v.Reverse()
            t = rh.Transform.Translation(v)
            pt_1.Transform(t)

        return math.sqrt(amount)

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

    # def get_circle(self):
    #     return rh.Circle(self.cp, self.radius)
    def get_rect(self):
        # Instead of generating a new circular agent, 
        # here generate a rectangle agent based on corner point
        a = rh.Point3d(self.cp.X-self.width*0.5 , self.cp.Y-self.height*0.5 , 0)
        b = rh.Point3d(self.cp.X+self.width*0.5 , self.cp.Y+self.height*0.5 , 0)
        rectangle = rh.Rectangle3d(self.plane, a, b)
        return rectangle

def run(pts, radii, max_iters, alpha):

    agents = []

    for i, pt in enumerate(pts):
        my_agent = Agent(pt, radii[i])
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
                total_amount += agent_1.collide(agent_2, alpha)

        if total_amount < .01:
            break

    iters = i

    print("process ran for {} iterations".format(i))

    circles = []

    for agent in agents:
        circles.append(agent.get_rect())

    return circles, iters
