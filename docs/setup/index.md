---
layout: default
title: Setting up
nav_order: 2
---

# Setting up your environment

In this tutorial we will develop a simple attractor point tutorial to make sure that our environment is set up and everything is working for the next tutorials.

Files you will need for this tutorial:

| Start with these files                  | In case you get lost, you can download the final solution here |
| :-------------------------------------- | :------------------------------------------------------------- |
| [0_start.3dm](data/0_setup/0_start.3dm) |                                                                |
| [0_start.gh](data/0_setup/0_start.gh)   | [0_end.gh](data/0_setup/0_end.gh)                              |

## Introduction

In this class you will use a set of programs and technologies to write our scripts, visualize their results, and submit the results of your work:

- **Rhino**: industry-standard computer modelling software with great support for custom scripting and development
- **Grasshopper**: visual programming environment for Rhino where you can create scripts and automations using an intuitive visual component-based UI
- **Python**: high-level programming language that supports Functional and Object-Oriented programming
- **Github**: version-control software for publishing and contributing to open source projects. Although you can use any git client or use git directly from the command line, I recommend using [Github Desktop](https://desktop.github.com/) which has version for both [Windows](https://central.github.com/deployments/desktop/desktop/latest/win32) and [MacOS](https://central.github.com/deployments/desktop/desktop/latest/darwin).

## Open the files

To start the tutorial, download the starting Rhino and Grasshopper files using the links above and open them. Make sure you see the "hello world!" message in the yellow `Panel`. This means that your Grasshopper and Python are working and you have everything you need for this tutorial.

![](images/0_01.png)

The `Python` component in the start file has already been set up with a set of four inputs which will be accessibile within the Python script:

<u>Inputs</u>

- x_num (`int`, "Item Access") - this number specifies the grid's x-dimension
- y_num (`int`, "Item Access") - this number specifies the grid's y-dimension
- spacing (`float`, "Item Access") - this number specifies the grid's spacing
- attractor (`Point3d`, "Item Access") - this point specifies the location of the attractor point

The `Python` component has also been set up with two outputs which we will populate with data within our script:

<u>Inputs</u>

- points - this will store a list of points representing the grid
- circles - this will tore a list of circles generated at each point of the grid

## Attractor point example

Let's develop the attractor point example to get an idea of how we will work with Python inside of Rhino Grasshopper. Double-click on the `Python` component to open the script. You will see that the `Rhino.Geometry` library has already been imported and the two output variables have been initialized as empty lists. Finally, there is a `print()` statement to display the test `hello world!` statement in the console.

```python
x = 5
def (ls):
    print "aha!"
```

## Challenge

# Workin with Github

In this class you will use Github to both access class files as well as submit your work for evaluation. Kind of like working on a wiki - explicit file change tracking.
