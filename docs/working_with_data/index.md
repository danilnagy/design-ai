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

Use the `Plane` command in Rhino to create a vertical surface 10 units wide and 15 units high.

{: .challenge-title }

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

Model and import surface, bring into Python

Get domains from surface

Create grid: double loop to extract nested lists of points from surface

Iterate over grid to create panel outlines - polylines, store in list and output to grasshopper

Planar surf panels

Move surface, observe that outlines break planarity

Ensure boundaries are planar - project corner point to plane along x-axis

Store new boundary in dict data structure

Extract both boundaries to gh

Loft to create edges

Offset

Extrude

Planar surf - panels still planar

Challenge 1 - extrude along panel normal
Challenge 2 - move minimal corner
