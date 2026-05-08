import pygame
import random
import time
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Maze:
    """
    A class to represent and manage the generation and solving of a rectangular maze.
    Uses the data structure: northWall[R][C] and eastWall[R][C].
    """
    def __init__(self, rows, cols):
        self.R = rows
        self.C = cols
        
        # northWall[i][j]: top wall of cell (i, j). 
        # northWall[0][j] is the bottom edge of the maze.
        self.north_walls = [[1 for _ in range(cols + 1)] for _ in range(rows + 1)]
        
        # eastWall[i][j]: right wall of cell (i, j).
        # eastWall[i][0] is the left edge of the maze.
        self.east_walls = [[1 for _ in range(cols + 1)] for _ in range(rows + 1)]
        
        # For generation
        self.visited_gen = [[False for _ in range(cols + 1)] for _ in range(rows + 1)]
        self.gen_stack = []
        self.gen_current = (random.randint(1, rows), random.randint(1, cols))
        self.visited_gen[self.gen_current[0]][self.gen_current[1]] = True
        self.gen_done = False
        
        # For solving
        self.solve_stack = []
        self.solve_current = None
        self.solve_target = None
        self.visited_solve = set()
        self.dead_ends = set()
        self.solve_done = False
        self.started_solving = False

    def get_unvisited_neighbors(self, r, c):
        neighbors = []
        # North
        if r < self.R and not self.visited_gen[r + 1][c]:
            neighbors.append(('N', r + 1, c))
        # South
        if r > 1 and not self.visited_gen[r - 1][c]:
            neighbors.append(('S', r - 1, c))
        # East
        if c < self.C and not self.visited_gen[r][c + 1]:
            neighbors.append(('E', r, c + 1))
        # West
        if c > 1 and not self.visited_gen[r][c - 1]:
            neighbors.append(('W', r, c - 1))
        return neighbors

    def generate_step(self):
        """Perform one step of the DFS maze generation."""
        if self.gen_done:
            return

        r, c = self.gen_current
        neighbors = self.get_unvisited_neighbors(r, c)

        if neighbors:
            # Choose one randomly
            direction, nr, nc = random.choice(neighbors)
            
            # Eat the wall
            if direction == 'N':
                self.north_walls[r][c] = 0
            elif direction == 'S':
                self.north_walls[r - 1][c] = 0
            elif direction == 'E':
                self.east_walls[r][c] = 0
            elif direction == 'W':
                self.east_walls[r][c - 1] = 0

            # 1 in 20 chance to eat an extra wall (Bonus: Cycles)
            if random.random() < 0.05:
                extra_neighbors = [('N', r, c), ('S', r-1, c), ('E', r, c), ('W', r, c-1)]
                edir, er, ec = random.choice(extra_neighbors)
                if edir in ['N', 'S'] and 0 < er < self.R and 0 < ec <= self.C:
                    self.north_walls[er][ec] = 0
                elif edir in ['E', 'W'] and 0 < er <= self.R and 0 < ec < self.C:
                    self.east_walls[er][ec] = 0

            # Push current to stack and move
            self.gen_stack.append((r, c))
            self.gen_current = (nr, nc)
            self.visited_gen[nr][nc] = True
        elif self.gen_stack:
            # Backtrack
            self.gen_current = self.gen_stack.pop()
        else:
            self.gen_done = True
            # Open start and end
            self.solve_current = (random.randint(1, self.R), 1) # Start on left
            self.east_walls[self.solve_current[0]][0] = 0 # Open left wall
            self.solve_target = (random.randint(1, self.R), self.C) # End on right
            self.east_walls[self.solve_target[0]][self.C] = 0 # Open right wall
            self.solve_stack.append(self.solve_current)
            self.visited_solve.add(self.solve_current)

    def solve_step(self):
        """Perform one step of the backtracking solver."""
        if self.solve_done or not self.started_solving:
            return

        r, c = self.solve_current
        if (r, c) == self.solve_target:
            self.solve_done = True
            return

        # Possible moves (no walls and not visited)
        moves = []
        # North
        if r < self.R and self.north_walls[r][c] == 0 and (r+1, c) not in self.visited_solve and (r+1, c) not in self.dead_ends:
            moves.append((r + 1, c))
        # South
        if r > 1 and self.north_walls[r - 1][c] == 0 and (r-1, c) not in self.visited_solve and (r-1, c) not in self.dead_ends:
            moves.append((r - 1, c))
        # East
        if c < self.C and self.east_walls[r][c] == 0 and (r, c+1) not in self.visited_solve and (r, c+1) not in self.dead_ends:
            moves.append((r, c + 1))
        # West
        if c > 1 and self.east_walls[r][c - 1] == 0 and (r, c-1) not in self.visited_solve and (r, c-1) not in self.dead_ends:
            moves.append((r, c - 1))

        if moves:
            # Choose a random move
            next_move = random.choice(moves)
            self.solve_stack.append(next_move)
            self.visited_solve.add(next_move)
            self.solve_current = next_move
        elif self.solve_stack:
            # Backtrack: mark as dead end
            self.dead_ends.add(self.solve_current)
            self.solve_stack.pop()
            if self.solve_stack:
                self.solve_current = self.solve_stack[-1]
        else:
            # No path? (Shouldn't happen in a proper maze)
            self.solve_done = True

    def render(self, display_width, display_height):
        """Render the maze using OpenGL."""
        scale_x = display_width / (self.C + 2)
        scale_y = display_height / (self.R + 2)
        offset_x = scale_x
        offset_y = scale_y

        # Draw Grid/Walls
        glColor3f(0.0, 0.0, 0.0) # Black walls
        glLineWidth(2.0)
        glBegin(GL_LINES)
        
        # Draw North Walls
        for r in range(self.R + 1):
            for c in range(1, self.C + 1):
                if self.north_walls[r][c]:
                    glVertex2f(offset_x + (c - 1) * scale_x, offset_y + r * scale_y)
                    glVertex2f(offset_x + c * scale_x, offset_y + r * scale_y)
        
        # Draw East Walls
        for r in range(1, self.R + 1):
            for c in range(self.C + 1):
                if self.east_walls[r][c]:
                    glVertex2f(offset_x + c * scale_x, offset_y + (r - 1) * scale_y)
                    glVertex2f(offset_x + c * scale_x, offset_y + r * scale_y)
        glEnd()

        # Draw Generation Cursor
        if not self.gen_done:
            r, c = self.gen_current
            glColor3f(0.0, 1.0, 0.0) # Green cursor for generator
            glPointSize(10.0)
            glBegin(GL_POINTS)
            glVertex2f(offset_x + (c - 0.5) * scale_x, offset_y + (r - 0.5) * scale_y)
            glEnd()

        # Draw Solution Path (Red Dot)
        if self.started_solving:
            # Draw dead ends (Blue dots)
            glColor3f(0.0, 0.0, 1.0)
            glPointSize(5.0)
            glBegin(GL_POINTS)
            for dr, dc in self.dead_ends:
                glVertex2f(offset_x + (dc - 0.5) * scale_x, offset_y + (dr - 0.5) * scale_y)
            glEnd()

            # Draw current path
            glColor3f(1.0, 0.0, 0.0)
            glPointSize(8.0)
            glBegin(GL_POINTS)
            for sr, sc in self.solve_stack:
                glVertex2f(offset_x + (sc - 0.5) * scale_x, offset_y + (sr - 0.5) * scale_y)
            glEnd()

def main():
    pygame.init()
    display_size = (800, 600)
    screen = pygame.display.set_mode(display_size, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Maze Generator & Solver")

    # OpenGL Setup
    glClearColor(1.0, 1.0, 1.0, 1.0) # White background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, display_size[0], 0, display_size[1])
    
    maze = Maze(20, 30) # R rows, C columns
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and maze.gen_done:
                    maze.started_solving = True
                if event.key == pygame.K_r: # Reset
                    maze = Maze(20, 30)

        # Logic
        if not maze.gen_done:
            maze.generate_step()
        elif maze.started_solving and not maze.solve_done:
            maze.solve_step()

        # Rendering
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        maze.render(display_size[0], display_size[1])
        pygame.display.flip()
        
        # Slow down for visualization
        if not maze.gen_done:
            clock.tick(120) # Speed of generation
        else:
            clock.tick(30) # Speed of solving

    pygame.quit()

if __name__ == "__main__":
    main()
