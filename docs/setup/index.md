import Rhino.Geometry as rh

d_1 = srf.Domain(0)
d_2 = srf.Domain(1)

print(d_1.Min, d_1.Max)
print(d_2.Min, d_2.Max)

u_spacing = (d_1.Max - d_1.Min) / u_num
v_spacing = (d_2.Max - d_2.Min) / v_num

print u_spacing, v_spacing

pts = []

for u in range(u_num + 1):
    pts.append([])
    for v in range(int(v_num + 1)):
        pt = srf.PointAt(u * u_spacing, v * v_spacing)
        pts[-1].append(pt)

polys = []

for i, row in enumerate(pts[:-1]):
    for j, pt_1 in enumerate(row[:-1]):

        polys.append({})

        pt_2 = row[j+1]
        next_row = pts[i+1]
        pt_3 = next_row[j+1]
        pt_4 = next_row[j]

        poly = rh.PolylineCurve([pt_1, pt_2, pt_3, pt_4, pt_1])
        polys[-1]["original"] = poly

        ## CHALLENGE 1: here we always move the same point (pt_3). To solve this challenge, make a loop that iterates over every options of
        ## corner point and tests how far each needs to move to be planar with the other three points. Then after the loops has run,
        ## create the boundary polyline using the case with the least distance

        ###pt_5 = rh.Point3d(pt_3)
        ###pl = rh.Plane(pt_1, pt_2, pt_4)

        pt_1_pt = rh.Point3d(pt_1)
        pt_2_pt = rh.Point3d(pt_2)
        pt_3_pt = rh.Point3d(pt_3)
        pt_4_pt = rh.Point3d(pt_4)

        pl_1 = rh.Plane(pt_2, pt_3, pt_4)
        t_1 = rh.Transform.PlanarProjection(pl_1)
        pt_1_pt.Transform(t_1)

        pl_2 = rh.Plane(pt_1, pt_3, pt_4)
        t_2 = rh.Transform.PlanarProjection(pl_2)
        pt_2_pt.Transform(t_1)

        pl_1 = rh.Plane(pt_1, pt_2, pt_4)
        t_1 = rh.Transform.PlanarProjection(pl_3)
        pt_3_pt.Transform(t_3)

        pl_4 = rh.Plane(pt_1, pt_2, pt_3)
        t_4 = rh.Transform.PlanarProjection(pl_4)
        pt_4_pt.Transform(t_4)

        ##dictionary
        polys - planar
        polys - edge

        if pt_1's DistanceTo pt_1_pt > pt_2's DistanceTo pt_2_pt and pt_1 etc.
                append plane
                if distance is > 0.01
                        append edge
        

        ## CHALLENGE 2: here we are using a PlanarProjection to move the point to its closest location on the plane.
        ## To move the point instead in the direction of the surface normal at that point, you can first use the srf.ClosestPoint() method to
        ## find the U and V coordinates at the corner point and then the srf.NormalAt() method to get the normal vector at that location.
        ## Finally, to find the location of the point you can create a line starting at the corner point and going in the direction of the
        ## normal, and then intersect this line with the plane using rh.Intersect.Intersection.LinePlane() to get the point. By definition
        ## this point will be planar with the other three points and aligned with the original point along the surface normal.

        ##pl_1 = rh.Plane(pt_2, pt_3, pt_4)
        ##t_1 = rh.Transform.PlanarProjection(pl_1)
        ##pt_1_pt.Transform(t_1)

        ##if pt_1's srf.ClosestPoint pt_1_pt > pt_2's DistanceTo pt_2_pt and pt_1 etc.

        t = rh.Transform.PlanarProjection(pl)
        pt_5.Transform(t)

        planar_poly = rh.PolylineCurve([pt_1, pt_2, pt_5, pt_4, pt_1])
        polys[-1]["planar"] = planar_poly

        polys[-1]["edge"] = []
        if pt_3.DistanceTo(pt_5) > 0.01:
            polys[-1]["edge"].append(rh.PolylineCurve([pt_2, pt_5, pt_3, pt_2]))
            polys[-1]["edge"].append(rh.PolylineCurve([pt_4, pt_3, pt_5, pt_4]))

original = [poly["original"] for poly in polys]
planar = [poly["planar"] for poly in polys]
edge = [poly["edge"] for poly in polys]