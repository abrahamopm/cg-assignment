# CG Assignment 1: Building and Running Mazes

| Name | ID | Section |
| :--- | :--- | :--- |
| Abraham Nigatu Kebede | UGR/7532/16 | 2 |

---

## Project Overview
This project implements the generation and traversal of a **proper maze**—a structure where every cell is connected to every other cell by a unique path.The application uses specific data structures to manage wall integrity and dynamic movement.

## Core Features

### 1. Maze Generation
* **Logic:** Employs a stack-based **Depth-First Search (DFS)** algorithm.
* **Process:** An invisible "mouse" eats through walls of a solid grid to connect adjacent unvisited cells.
* **Backtracking:** If the mouse hits a dead end, it pops a previously saved candidate cell from the stack to continue until all cells are visited.

### 2. Maze Solver
* **Algorithm:** Uses a **backtracking algorithm** to find the path from the starting edge to the ending edge.
* **Visualization:** * **Red Dot:** Represents the current active path of the mouse.
    * **Blue Dot:** Marks dead ends that have been explored and discarded.
## Demonstration
The video demonstration showing the dynamic "eating" process and the functional solver is available below:

**[Watch the Loom Recording](https://drive.google.com/file/d/1E-ui4mSF11XakcyJ1UmXbO2UGYm4Ke4R/view?usp=sharing)**

*Note: This file is also attached to the classroom assignment.*
