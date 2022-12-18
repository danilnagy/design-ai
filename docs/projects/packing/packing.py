import sys
import Rhino.Geometry as rh
from scriptcontext import doc
import json

class Agent:

    def __init__(self, pt, r):
    def __init__(self, pt, r, name, adjcs):

        self.cp = pt
        self.radius = r
        self.neighbors = []
        self.name = name
        self.adjacency = adjcs

    # method for adding another instance to a list of neighbors
    def add_neighbor(self, other):

        self.neighbors.append(other)

    # method for checking distance to other room object and moving apart if they are overlapping
@@ -87,23 +90,36 @@ def cluster(self, other, alpha):

        return amount

    def get_circle(self):
        return rh.Circle(self.cp, self.radius)
    def get_circle(self, plane):
        #return rh.Circle(self.cp, self.radius)
        return rh.Rectangle3d(plane, self.radius, self.radius)


def run(pts, radii, max_iters, alpha, adjacencies):
def run(pts, radii, names, adjacencies, max_iters, alpha):

    print(adjacencies)
    print(names)

    agents = []

    for i, pt in enumerate(pts):
        my_agent = Agent(pt, radii[i])

        print(names[i])

        my_agent = Agent(pt, radii[i], names[i], adjacencies[names[i]])
        agents.append(my_agent)

    # for each agent in the list, add the previous agent as its neighbor
        print(names[i])

    #for each agent add all adjacency agents as its neighbor
    for i in range(len(agents)):
        agents[i].add_neighbor(agents[i-1])

        for j in range(len(agents)):

            if agents[j].name in agents[i].adjacency:
                agents[i].add_neighbor(agents[j])
            else:
                continue

    for i in range(max_iters):

@@ -117,18 +133,17 @@ def run(pts, radii, max_iters, alpha, adjacencies):

            # collide with all agents after agent in list
            for agent_2 in agents[j+1:]:
                # add extra multiplier to decrease effect of cluster
                total_amount += agent_1.collide(agent_2, alpha/5)
                # add extra multiplier to decrease effect of cluster (change)
                total_amount += agent_1.collide(agent_2, alpha/4)

        if total_amount < .01:
            break

    iters = i

    print("process ran for {} iterations".format(i))

    circles = []

    # append circles in Rhino
    for agent in agents:
        circles.append(agent.get_circle())

docs/recursive_systems/index.md
Viewed
@@ -256,46 +256,60 @@ branches = grow([rh.Point3d(0,0,0)], params) ## passing the starting point as th

import sys
import Rhino.Geometry as rh
from scriptcontext import doc
import json

def grow(pts, params):
    
    if len(params) <= 0:
        return []
    
    param = params.pop(0)
    start_pt = pts.pop(0)
    
    lines = []
    
    if param == 1:
        new_pt = rh.Point3d(start_pt)
        new_pt.Transform(rh.Transform.Translation(0,0,1))
        lines.append(rh.Line(start_pt, new_pt))
        pts.append(new_pt)
        
        return lines + grow(pts, params)
    
    elif param == 2:
        new_pt_1 = rh.Point3d(start_pt)
        new_pt_1.Transform(rh.Transform.Translation(0,1,1))
        lines.append(rh.Line(start_pt, new_pt_1))
        pts.append(new_pt_1)
        
        new_pt_2 = rh.Point3d(start_pt)
        new_pt_2.Transform(rh.Transform.Translation(0,-1,1))
        lines.append(rh.Line(start_pt, new_pt_2))
        pts.append(new_pt_2)
        
        return lines + grow(pts, params)
    
    elif param == 3:
        
        new_pt_3 = rh.Point3d(start_pt)
        new_pt_3.Transform(rh.Transform.Translation(1,0,1))
        lines.append(rh.Line(start_pt, new_pt_3))
        pts.append(new_pt_3)
        
        new_pt_4 = rh.Point3d(start_pt)
        new_pt_4.Transform(rh.Transform.Translation(-1,0,1))
        lines.append(rh.Line(start_pt, new_pt_4))
        pts.append(new_pt_4)
        
        
        return lines + grow(pts, params)
        
        
        ### ADD CODE HERE TO DEFINE BEHAVIOR FOR THE PARAMETER '3' ###
        
        return lines
    
    else:
        return lines
@@ -327,9 +341,11 @@ Inside the `Python` script you will find two functions already defined:

Currently, the boundaries are directly output to the curves output. What we need to do is write another function called `split_recursively` which calls the `split_space()` function recursively to progressively subdivide the input space into a set of smaller spaces. Then we can call this function with our initial boundaries and parameter sets to perform the subdivision. Here is the final script once the function is implemented:

```python
```python lr3102
import Rhino.Geometry as rh
from scriptcontext import doc
import math
import rhinoscriptsyntax as rs
# get absolute and angle tolerances from document
abs_tol = doc.ModelAbsoluteTolerance
@@ -339,51 +355,51 @@ ang_tol = doc.ModelAngleToleranceRadians
def split_curve(c1, c2, close):
    # get intersection events between two curves
    inter = rh.Intersect.Intersection.CurveCurve(c1, c2, abs_tol, abs_tol)
    
    # get parameters on first curve from all intersection events
    # this code uses a "list comprehension" which is a shortcut for iterating over a list in Python
    # this single line does the same thing as:
    
    # p = []
    # for i in range(inter.Count):
        # p.append(inter[i].ParameterA)
    
    p = [inter[i].ParameterA for i in range(inter.Count)]
    
    # handle multiple intersections (for non-convex boundaries)
    
    # if more than two parameters are returned, it means that the boundary shape is non-convex
    # and was split by the split line into more than two pieces
    # since we only want two pieces, we must find two consecutive parameters
    # since we only want two pieces, we must find two consecutive parameters 
    # which split the boundary into only two separate pieces
    
    if len(p) > 2:
        
        # loop over all parameters
        for i in range(len(p)):
            
            # get the points at the previous and current parameters in the list
            pt1 = c1.PointAt(p[i-1])
            pt2 = c1.PointAt(p[i])
            
            # get the line between the two points
            l = rh.Line(pt1, pt2).ToNurbsCurve()
            
            # check how many times the line intersects the boundary
            inter = rh.Intersect.Intersection.CurveCurve(c1, l.ToNurbsCurve(), abs_tol, abs_tol)
            # if there are only two intersections, return the two parameters
            
            # if there are only two intersections, return the two parameters 
            # and break out of loop
            if len(inter) == 2:
                p = [p[i-1], p[i]]
                break
    
    # split the curve by the parameters
    pieces = c1.Split(p)
    
    # create a new list to store the final curves
    curves = []
    
    # iterate over pieces
    for piece in pieces:
        # if closed curves were requested and the curve is not closed
@@ -394,78 +410,98 @@ def split_curve(c1, c2, close):
        else:
            # otherwise add the original piece to the curves list
            curves.append(piece)
    
    # return the final curves
    return curves
# this function splits a space with two parameters
def split_space(curve, dir, param):
def split_space(curve, dir, param, deg):
    
    # get the bounding box of the curve
    bb = curve.GetBoundingBox(True)
    # get the base point of the bounding box
    base_pt = rh.Point3d(bb.Min.X, bb.Min.Y, 0.0)
    
    # get the x and y dimensions of the bounding box
    x = bb.Max.X - bb.Min.X
    y = bb.Max.Y - bb.Min.Y
    
    # create a list of the x,y dimensions and x,y unit vectors
    dims = [x,y]
    vecs = [rh.Vector3d(1,0,0), rh.Vector3d(0,1,0)]
    
    # create a vector to position the split line based on the two parameters
    vec_1 = vecs[dir] * dims[dir] * param
    
    # copy the base point
    new_pt_1 = rh.Point3d(base_pt)
    # move the new point according to the vector
    new_pt_1.Transform(rh.Transform.Translation(vec_1))
    
    # calculate the opposite of the dir parameter
    # if the parameter is 0 this results in 1, if 1 then 0
    other_dir = abs(dir-1)
    
    # create a vector in the other direction the full extent of the bounding box
    vec_2 = vecs[other_dir] * dims[other_dir]
    
    # create a copy of the moved point
    new_pt_2 = rh.Point3d(new_pt_1)
    # move the point to define the other end point of the split line
    new_pt_2.Transform(rh.Transform.Translation(vec_2))
    
    # create the split line and convert it to a Nurbs Curve
    # (this is necessary to make the splitting work in the next function)
    split_line = rh.Line(new_pt_1, new_pt_2).ToNurbsCurve()
    
    #find split line center point
    sl_length = rh.Line(new_pt_1, new_pt_2).Length
    sl_mid = rh.Line(new_pt_1, new_pt_2).PointAtLength(sl_length/2)
    
    #create line rotation angle
    rotation = deg*math.pi/180
    
    #rotate split line by rads
    split_line.Transform(rh.Transform.Rotation(rotation,sl_mid))
    
    # use the split_curve() function to split the boundary with the split line
    parts = split_curve(curve, split_line, True)
    
    # return the curves resulting from the split
    return parts
# this function calls the split_space() function recursively
# to continuosly split an input curve into parts based on a set of parameters
def split_recursively(curves, dirs, params):
def split_recursively(curves, dirs, params, degs):
    
    # if there are no more parameters in the list, return the input curves
    if len(dirs) <= 0 or len(params) <= 0:
        return curves
    
    # get the first parameters and the first curve from the input lists
    dir = dirs.pop(0)
    param = params.pop(0)
    curve = curves.pop(0)
    
    #deg = 45 
    #this option works only because i know from the rhino geometry the inclination of my angle, but if I have multiple geometry with different inclinations it's not correct
    
    # I set up a 1-360 list of values that you change manually.
    # the goal was to be able to set the angle of the drawn geometry "boundary" with respect to a baseline (0,1,0) and set it as a deg parameter, but I was not successful in doing it
    
    deg = degs.pop(0)
   
    
    # split the curve and add the results to the curves list
    curves += split_space(curve, dir, param)
    curves += split_space(curve, dir, param, deg)
    
    # run the split_recursively() function again with the updated curves list and the remaining parameters
    return split_recursively(curves, dirs, params)
    return split_recursively(curves, dirs, params, degs)
# call the split_recursively() function to split the input boundary into parts
# this starts the recursion process with all the parameters and a single curve in the input list
curves = split_recursively([boundary], dirs, params)
curves = split_recursively([boundary], dirs, params, degs)
```