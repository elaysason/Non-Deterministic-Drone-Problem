# Non-Deterministic-Drone-Problem
In this problem we are the head of a delivery agency and try to deliver the packages in the shortest time possible. Our clients are moving across the grid in a non-deterministic manner.

1. [General](#General)
    - [Program Structure](https://github.com/elaysason/Deterministic-Drone-Problem/blob/main/README.md#program-structure)  
2. [Installation](#Installation)

## General
The environment is a rectangular grid with passable and non passable points for drone passage.Moreover, there are packages lying in different locations
around the grid. The packages can be picked up by drones and delivered to clients. Clients behavior is determined by starting location and the probability to move in each direction (up, down, left, right, or stay in place). The goal is to achieve the maximum amount of points, point are given for the following: 10 for delivery and -15 for resetting the environment.
### Program Structure

1. ex2.py - implementation of DroneAgent class which is used to determine to behavior of a drone, at each step of the game the next action is chosen according to the state of the game.
2. check.py - A file that includes some wrappers and inputs
3. search.py - A file that has implementations of different search algorithms (including
GBFS, A* and many more)
4. utils.py - A file that contains some utility functions.

### Installation
1. Open the terminal

2. Clone the project by:
```
    $ git clone https://github.com/elaysason/Non-Deterministic-Drone-Problem.git
```
3. Run the check.py file by:
```
    $ python3 check.py
```
