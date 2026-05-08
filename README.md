# Maze Generator and Solver

This project implements a rectangular maze generator and solver using PyOpenGL and Pygame.

## Features
- **Dynamic Maze Generation**: Uses a Depth-First Search (DFS) algorithm with a stack-based approach (the "mouse" logic) to create a perfect maze.
- **Backtracking Solver**: Implements a backtracking algorithm to find a path from a random start point on the left edge to a random end point on the right edge.
- **Visual Feedback**:
  - Green dot: The "mouse" eating through walls during generation.
  - Red dots: The current path being explored by the solver.
  - Blue dots: Dead ends identified and avoided by the solver.
- **Cycle Generation**: Occasionally eats extra walls (1 in 20 chance) to create cycles, making the maze non-tree-like and defeating simple "shoulder-to-the-wall" rules.
- **Modular Design**: The logic is encapsulated in a `Maze` class, separating the grid data structure, generation logic, solving logic, and rendering.

## Data Structure
The maze is represented using two 2D arrays:
- `northWall[R][C]`: Tracks whether the top wall of each cell is intact.
- `eastWall[R][C]`: Tracks whether the right wall of each cell is intact.
- Row 0 and Column 0 are used to represent the bottom and left edges of the maze respectively.

## How to Run
1. Ensure you have `pygame` and `PyOpenGL` installed:
   ```bash
   pip install pygame PyOpenGL
   ```
2. Run the program:
   ```bash
   python maze.py
   ```
3. Controls:
   - Watch the maze generate automatically.
   - Press **SPACE** once generation is finished to start the solver.
   - Press **R** to reset and generate a new maze.

## Implementation Details
- **Generation**: The "mouse" checks 4 neighbors. If unvisited, it chooses one randomly, eats the wall, and pushes the current location onto a stack. If stuck, it pops the stack to backtrack.
- **Solving**: The solver moves randomly into open adjacent cells. If it hits a dead end, it marks the cell blue and backtracks using a stack.
