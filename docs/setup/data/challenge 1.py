import Rhino.Geometry as rh

points = []
circles = []

for x in range(x_num):
    for y in range(y_num):
        point = rh.Point3d(x, y, 0.0)
        points.append(point)

        dist = point.DistanceTo(attractor)
        if dist < 3:
            radius= 0.2
        else:
            radius=0.6
        circle = rh.Circle(point, radius)
        circles.append(circle)



