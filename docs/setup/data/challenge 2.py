import Rhino.Geometry as rh

points = []
circles = []

for x in range(x_num):
    for y in range(y_num):
        point = rh.Point3d( spacing*x, spacing*y, 0.0)
        points.append(point)

        dist = point.DistanceTo(attractor)
        radius= dist / 5
        circle = rh.Circle(point, radius)
        circles.append(circle)



