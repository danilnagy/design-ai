---
layout: default
title: 1. Working with data
nav_order: 3
---

# Working with data

In this tutorial we will develop a parametric facade to explore various issues and techniques in working with data in Python.

Files you will need for this tutorial:

| Start with these files          | In case you get lost, you can download the final solution here |
| :------------------------------ | :------------------------------------------------------------- |
| [1_start.3dm](data/1_start.3dm) |                                                                |
| [1_start.gh](data/1_start.gh)   | [1_end.gh](data/1_end.gh)                                      |

## Introduction

### Step 1. Create the surface

The first step is to create a Surface which will define our facade. We will model this as a surface in the Rhino model and import it into Grasshopper so that we can later modify the surface and have the facade respond. To create the Surface object, use the `Plane` command in Rhino to create a vertical surface 10 units wide and 15 units high.

{: .note-title }

> Tip
>
> Use the context menus in the Rhino command line to change the way a command behaves as it's being executed. To create a vertical surface of a given dimension, you can issue the following commands in the Rhino command prompt in order, pressing `Enter` after each line:
>
> ```
> Plane
> V (for "Vertical")
> 0 (to start at origin)
> 10 (to lock the first dimension at 10 units, then click in the view to set the plane's base curve.)
> 15 (to lock the height, click on the canvas to confirm direction.)
> ```

![](images/1_01.png)

Now that we have the surface modelled we need to first import it into Grasshopper and then pass it into a `Python` component so we can start to work with it. First, use a `Geometry Pipeline` component to bring in the the surface by Layer name, then plug it into one of the inputs of a `Python` component. You can rename the input if you wish, just remember that the surface will be available through that variable name in the Python code. Also remember to set the _Type hint_ to **Surface** so that you can work directly with the object's geometry.

![](images/1_02.png)

### Step 2. Create the point grid

Let's start developing the code for this example. Double-click the `Python` component to open the code edit. Delete any code already there and on the first line import the `Rhino.Geometry` library:

```python
import Rhino.Geometry as rh
```

The first thing we need to do to build the facade is to arrange a two-dimensional grid of points evenly across the surface. These grid points will define the corners of the facade panels. To create the grid points we will use a double `for` loop similar to the [previous example](https://design-ai.net/docs/setup/). However, this time we will not be setting the spacing of the grid through a parameter. Instead, the spacing will be dictated by the desired number of panels in each direction as well as the dimensions of the surface itself.

To understand the spacing of the points on the grid, we need to know about its _Domain_ or the extents of the surface within its two-dimensional local coordinate system. This local coordinate system is unique to each surface, and any point on the surface can be designated as a location along its two dimensions. These dimensions are typically designated as `U` and `V` to differentiate from the `X`, `Y`, and `Z` coordinates of the three-dimensional global coordinate system.

{: .note }
Locating a point on a surface based on its local coordinate system should not be unfamiliar. It is the same way we locate places on the Earth. If we want to describe the location of a place we don't use it's absolute `XYZ` coordinates in the 3d space of the universe relative to the sun. Instead we use two coordinates (latitude and longitude) which run in two directions along the surface of the Earth. In a similar way, understanding curvature and local coordinate systems will help us locate points on the surface to place our panels.

To get the domain of the surface in its two directions, use the [`Domain()`](https://developer.rhino3d.com/api/RhinoCommon/html/M_Rhino_Geometry_Surface_Domain.htm) method of the [`Surface`](https://developer.rhino3d.com/api/RhinoCommon/html/T_Rhino_Geometry_Surface.htm) Class. This method takes in one input which is the direction (integer 0 or 1) and returns an instance of the `Domain` class. You can print the `Domain` objects to make sure that the represent the extents of the surface ([0,10] representing the 10 unit width and [0,15] representing the 15 unit height).

```python
d_1 = srf.Domain(0)
d_2 = srf.Domain(1)

print(d_1, d_2)
```

This should print something like this to the Output console:

```
(<Rhino.Geometry.Interval object at 0x000000000000003F [0,10]>, <Rhino.Geometry.Interval object at 0x0000000000000040 [0,15]>)
```

double loop to extract nested lists of points from surface

### Step 4. Create the panels

Iterate over grid to create panel outlines - polylines, store in list and output to grasshopper

Planar surf panels

Move surface, observe that outlines break planarity

### Step 5. Make the panels planar

Ensure boundaries are planar - project corner point to plane along x-axis

Store new boundary in dict data structure

Extract both boundaries to gh

Ensure planar srf works

### Step 6. Model the panels

Loft to create edges

Offset

Extrude

Planar surf - panels still planar

{: .challenge-title }

> Challenge 1
>
> extrude along panel normal.

{: .challenge-title }

> Challenge 2
>
> move minimal corner.

## Conclusion
