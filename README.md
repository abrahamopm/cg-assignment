# CG Assignment 1: Building and Running Mazes

| Name | ID | Section |
| :--- | :--- | :--- |
| Abraham Nigatu Kebede | UGR/7532/16 | 2 |

---

## Project Overview
[cite_start]This project implements the generation and traversal of a **proper maze**—a structure where every cell is connected to every other cell by a unique path[cite: 9, 10]. [cite_start]The application uses specific data structures to manage wall integrity and dynamic movement[cite: 11, 12].

## Core Features

### 1. Maze Generation
* [cite_start]**Logic:** Employs a stack-based **Depth-First Search (DFS)** algorithm[cite: 48].
* [cite_start]**Process:** An invisible "mouse" eats through walls of a solid grid to connect adjacent unvisited cells[cite: 20, 24].
* [cite_start]**Backtracking:** If the mouse hits a dead end, it pops a previously saved candidate cell from the stack to continue until all cells are visited[cite: 26, 27].

### 2. Maze Solver
* [cite_start]**Algorithm:** Uses a **backtracking algorithm** to find the path from the starting edge to the ending edge[cite: 32, 33].
* [cite_start]**Visualization:** * **Red Dot:** Represents the current active path of the mouse[cite: 36].
    * [cite_start]**Blue Dot:** Marks dead ends that have been explored and discarded[cite: 37].

## Demonstration
The video demonstration showing the dynamic "eating" process and the functional solver is available below:

**[Watch the Loom Recording](https://drive.google.com/file/d/1E-ui4mSF11XakcyJ1UmXbO2UGYm4Ke4R/view?usp=sharing)**

*Note: This file is also attached to the classroom assignment.*
