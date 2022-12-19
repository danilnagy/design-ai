import Rhino.Geometry as rh
from scriptcontext import doc

# get absolute and angle tolerances from document
abs_tol = doc.ModelAbsoluteTolerance
ang_tol = doc.ModelAngleToleranceRadians

# this function splits a curve c1 with another curve c2


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
            inter = rh.Intersect.Intersection.CurveCurve(
                c1, l.ToNurbsCurve(), abs_tol, abs_tol)

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
        if close == True and not piece.IsClosed:
            # create a new line to close the curve, join them together, and add the result to curves list
            line = rh.Line(piece.PointAtStart, piece.PointAtEnd).ToNurbsCurve()
            curves += rh.NurbsCurve.JoinCurves([piece, line])
        else:
            # otherwise add the original piece to the curves list
            curves.append(piece)

    # return the final curves
    return curves

# this function splits a space with two parameters


def split_space(curve, dir, param):

    # get the bounding box of the curve
    bb = curve.GetBoundingBox(True)
    # get the base point of the bounding box
    base_pt = rh.Point3d(bb.Min.X, bb.Min.Y, 0.0)

    # get the x and y dimensions of the bounding box
    x = bb.Max.X - bb.Min.X
    y = bb.Max.Y - bb.Min.Y

    # create a list of the x,y dimensions and x,y unit vectors
    dims = [x, y]
    vecs = [rh.Vector3d(1, 0, 0), rh.Vector3d(0, 1, 0)]

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

    # use the split_curve() function to split the boundary with the split line
    parts = split_curve(curve, split_line, True)

    # return the curves resulting from the split
    return parts

# this function calls the split_space() function recursively
# to continuosly split an input curve into parts based on a set of parameters


def split_recursively(curves, dirs, params):

    # if there are no more parameters in the list, return the input curves
    if len(dirs) <= 0 or len(params) <= 0:
        return curves

    # get the first parameters and the first curve from the input lists
    dir = dirs.pop(0)
    param = params.pop(0)
    curve = curves.pop(0)

    # split the curve and add the results to the curves list
    curves += split_space(curve, dir, param)

    # run the split_recursively() function again with the updated curves list and the remaining parameters
    return split_recursively(curves, dirs, params)
