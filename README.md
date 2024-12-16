# GOAT_ROBOTICS
Python , DSA  Algorithm

**Prompt_1**
**Dynamic Robot Navigation**
Problem Statement for Complex Robot Navigation Simulation
Objective: Design a complex robot navigation simulation within a 10x10 grid, where the robot must find its way from a given start point to a destination point while avoiding dynamically changing obstacles.

**Components:**
Grid Environment:

Create a 10x10 grid representing the environment.
Randomly generate 30 obstacles at the start of the simulation. These obstacles should move randomly every few seconds, creating a dynamic, real-time challenge for pathfinding.
Prompt the user to input the start and end points within the grid.
Ensure that the input points are within the bounds of the grid and not placed on obstacle cells.
Path Planning:

Implement a pathfinding algorithm (e.g., A*, D*, Dynamic Programming) optimized for the dynamic changes in the grid.
Adapts to constantly moving obstacles and finds the optimal path.
Optimize for real-time responsiveness by comparing execution time of different algorithms under dynamic conditions.
Obstacle Dynamics:

Implement an obstacle movement system where obstacles move randomly at a set interval (e.g., every 3-5 seconds).
Unpredictable movement of obstacles requires the robot to continuously adjust its path.
Output Visualization:

Display a real-time animation of the robot navigating the grid.
Highlight obstacles, the robot’s path, and dynamically changing terrains.
Show the coordinates of the robot’s path as it moves through the grid.
Visually demonstrate the adaptive behavior of the robot when obstacles move or new obstacles are introduced during navigation.
Tools and Technologies:
Programming language: Suitable for robot navigation (e.g., Python, C++)
Real-world implementation: Can use ROS-compatible robots like TurtleBot for demonstration or PyGame for a simulated environment.

**Prompt_2
Robot Navigation with Obstacles **

Objective: Design and implement an autonomous robot navigation algorithm to move from a starting position to the center of a rectangular pillar, avoiding obstacles and adhering to strict movement constraints (no diagonal movement). The robot must navigate in a dynamic environment and calculate an optimal path while updating its position iteratively.

Setup:
Pillar Definition: Given coordinates of the four vertices of a rectangular pillar.
Robot Position: Starts outside the pillar and needs to navigate to its center.
Dynamic Environment: The environment may change over time, requiring real-time path replanning.
Tasks:
Calculate Center: Compute the geometric center of the pillar using the given vertex coordinates.
Path Planning: Develop a navigation algorithm that avoids the pillar and other obstacles, moving only in straight lines (no diagonal movements).
Displacement Calculation: Ensure the robot moves step-by-step, minimizing travel distance and avoiding collisions.
Constraints:
No diagonal movement.
Find the shortest path while avoiding collisions.
Adapt to real-time changes in the environment (e.g., new obstacles).
Ensure safe distance from the pillar and obstacles.
Deliverables:
Simulation/Demonstration: Show the robot successfully navigating to the center of the pillar.
Algorithm Documentation: Explain the center calculation, pathfinding, and collision avoidance.
Presentation: Detail the approach, challenges, and solutions.
Tools and Technologies:
Programming language: Suitable for robot navigation (e.g., Python, C++)
Real-world implementation: Can use ROS-compatible robots like TurtleBot for demonstration or PyGame for a simulated environment. ROS is preferred for real-world demonstrations.
