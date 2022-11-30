---
layout: default
title: Final project
nav_order: 6
---

# Final project

In this section we will explore the concepts of emergence and agent-based behavior and learn how we can program them in Python using dynamic and object-oriented programming.

## Introduction

Agent-based systems are often used to model complex behaviors in nature, which are also typically defined by the interaction of a large number of agents who are driven by a relatively simple set of rules. Examples of such systems include the flocking of birds, the organization of ants, the growth of slime mold, and the construction of termite mounds. These types of systems are often called _emergent_ because of their ability to develop highly complex behaviors and structures from a set of relatively simple behaviors.

![](images/3_04.gif)

| Files you will need for this tutorial | al                                                                                 |
| :------------------------------------ | ---------------------------------------------------------------------------------- |
| SUBD {: .label .label-green }         | [Code](https://github.com/danilnagy/design-ai/tree/gh-pages/docs/projects/packing) |
|                                       | [Open issues](https://github.com/danilnagy/design-ai/labels/subd)                  |

To start, open the file above within a new Rhino document. In the model, the first set of Grasshopper components create a list of points based on parameters created by a `Gene Pool` component. These points are input into a Python component that contains a script defining a single class called `Agent` that has the following properties and methods:

SUBD {: .label .label-green }: https://github.com/danilnagy/design-ai/labels/subd
: https://github.com/danilnagy/design-ai/labels/packing
