# mazeexplorer

Maze Explorer and Solver Visualizer

This project is a dynamic, grid-based application built using Python and Pygame. It functions as both an interactive game and an algorithmic visualization tool, allowing users to compare their problem-solving approach against deterministic shortest-path algorithms.

Features

    Dynamic Maze Generation
    Uses the Recursive Backtracker algorithm for maze creation.
    Includes an additional braiding step to create an imperfect maze with loops and multiple possible routes.
    Ensures each playthrough generates a unique challenge.
    Continuous Player Movement
    Implements smooth, continuous movement based on arrow key holding.
    Designed for responsive control in a grid environment.
    Dual Visualization and Path Comparison
    Upon reaching the goal, the system computes and displays three distinct paths:
    Optimal Path (BFS): The shortest possible path.
    Player Path: The route actually taken by the user.
    DFS Path: A typically longer, non-optimal route for comparison.
    Professional Information Panel
    Includes a clean side dashboard inspired by classic Tetris layout.
    Displays game statistics and path comparison results without obstructing gameplay.
    Getting Started


Prerequisites

    Python 3.x
    Pygame library
    Install Pygame using:
    pip install pygame
    Installation and Setup

This project requires the following two files placed in the same directory:

    maze_data.py
    Contains maze generation logic and constants.
    main.py
    Contains the main game loop, player control logic, and visualization features.

How to Run

    Navigate to the project directory in your terminal and execute:
    python main.py

How to Play

    Control	Action
    Arrow Keys (↑ ↓ ← →)	Move the red player circle
    Reach Blue Square	Complete the maze
    Spacebar	After winning, closes results panel and exits
    Game Objective

The game is a spatial reasoning challenge. Once the player reaches the goal, a results panel appears displaying:

    Optimal Path (BFS): Minimum number of steps possible.
    Your Path: Steps taken by the player.
    DFS Path: A longer, non-optimal comparison route.


