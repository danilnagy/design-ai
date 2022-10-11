---
layout: default
title: 2. Recursive Systems
nav_order: 4
---

# Recursive Systems

In this tutorial we will explore recursive systems through a branching and subdivision tutorial.

Files you will need for this tutorial:

| Start with these files          | In case you get lost, you can download the final solution here |
| :------------------------------ | :------------------------------------------------------------- |
| [2_start.3dm](data/2_start.3dm) | [2_end.3dm](data/2_end.3dm)                                    |
| [2_start.gh](data/2_start.gh)   | [2_end.gh](data/2_end.gh)                                      |

## Introduction

In computer science, ‘recursion’ refers to a strategy where the solution to a problem can be solved using solutions to smaller versions of the same problem. In computer programming, such systems are defined using ‘recursive functions’ which are basically functions that can call themselves. These kinds of functions are impossible to define in Grasshopper because there is no way to feed data from a function back into itself. Using Python, however, we can easily create such functions by having the function define its output based on the outputs of modified versions of itself.

These ‘recursive’ calls to the same function create a kind of spiral behavior defined by subsequent executions of different versions of the same function. By default this recursive behavior will create an infinite spiral, similar to the infinite ‘while’ loop we saw in a previous section. If you don’t provide any way for the recursion to stop, the function will keep calling itself for eternity, which will simply cause your script to crash. We can prevent this by defining a conditional inside the function that specifies a ‘termination criteria’ which stops the function from calling itself. Once the final function call has terminated, its return is fed all the way back through all the function calls until the final solution is returned.

The concept of recursion is incredibly powerful, and there are many useful application for recursion in computer programming. At the same time, the nested behavior of recursive functions can be difficult for people to understand intuitively, which is why recursion tends to be a difficult subject for people just starting out in programming. To start to gain an intuition for how recursive functions work, let’s create a simple example of a recursive function that can add a sequence of numbers up to a certain value. We won’t be using any geometry yet, but you can try this code directly in a Python node in Grasshopper.
