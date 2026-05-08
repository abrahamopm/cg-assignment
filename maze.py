import pygame
import random
import time
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Maze:
    """
    A class to manage a rectangular maze.
    Data Structure:
    - north_walls[r][c]: Wall above cell (r, c). north_walls[0] is bottom boundary.
    - east_walls[r][c]: Wall to the right of cell (r, c). east_walls[r][0] is left boundary.
    """
    def __init__(self, rows, cols):
        self.R = rows
        self.C = cols
        
        # Initialize all walls as intact (1)
        # Dimensions are (R+1) x (C+1) to handle boundaries correctly
        self.north_walls = [[1 for _ in range(cols + 1)] for _ in range(rows + 1)]
        self.east_walls = [[1 for _ in range(cols + 1)] for _ in range(rows + 1)]
        
        # Generation State
        self.visited_gen = [[False for _ in range(cols + 1)] for _ in range(rows + 1)]
        self.gen_stack = []
        # Start at a random cell within bounds [1, R] and [1, C]
        start_r, start_c = random.randint(1, rows), random.randint(1, cols)
        self.gen_current = (start_r, start_c)
        self.visited_gen[start_r][start_c] = True
        self.gen_done = False
        
        # Solving State
        self.solve_stack = []
        self.solve_current = None
        self.solve_target = None
        self.visited_solve = set()
        self.dead_ends = set()
        self.solve_done = False
        self.started_solving = False
        self.status = "Generating..."

    def get_unvisited_neighbors(self, r, c):
        """Find adjacent cells that haven't been visited during generation."""
        neighbors = []
        if r < self.R and not self.visited_gen[r + 1][c]: neighbors.append(('N', r + 1, c))
        if r > 1 and not self.visited_gen[r - 1][c]: neighbors.append(('S', r - 1, c))
        if c < self.C and not self.visited_gen[r][c + 1]: neighbors.append(('E', r, c + 1))
        if c > 1 and not self.visited_gen[r][c - 1]: neighbors.append(('W', r, c - 1))
        return neighbors

    def generate_step(self):
        """One step of DFS generation."""
        if self.gen_done: return

        r, c = self.gen_current
        neighbors = self.get_unvisited_neighbors(r, c)

        if neighbors:
            direction, nr, nc = random.choice(neighbors)
            # Remove the wall between current and neighbor
            if direction == 'N': self.north_walls[r][c] = 0
            elif direction == 'S': self.north_walls[r - 1][c] = 0
            elif direction == 'E': self.east_walls[r][c] = 0
            elif direction == 'W': self.east_walls[r][c - 1] = 0

            # Optional: Bonus cycle generation (1 in 50 for stability)
            if random.random() < 0.02:
                # Pick a random internal wall to remove
                er, ec = random.randint(1, self.R), random.randint(1, self.C)
                if random.choice([True, False]):
                    if er < self.R: self.north_walls[er][ec] = 0 # Not top boundary
                else:
                    if ec < self.C: self.east_walls[er][ec] = 0 # Not right boundary

            self.gen_stack.append((r, c))
            self.gen_current = (nr, nc)
            self.visited_gen[nr][nc] = True
        elif self.gen_stack:
            self.gen_current = self.gen_stack.pop()
        else:
            # Generation complete: setup solver
            self.gen_done = True
            self.status = "Finished! Press SPACE to solve."
            self.init_solver()

    def init_solver(self):
        """Pick start/end and initialize solver variables."""
        # Start on left edge (col 1), End on right edge (col C)
        start_r = random.randint(1, self.R)
        end_r = random.randint(1, self.R)
        
        self.solve_current = (start_r, 1)
        self.solve_target = (end_r, self.C)
        
        # Open the entrance and exit walls
        self.east_walls[start_r][0] = 0
        self.east_walls[end_r][self.C] = 0
        
        self.solve_stack = [self.solve_current]
        self.visited_solve = {self.solve_current}

    def solve_step(self):
        """One step of backtracking solver."""
        if self.solve_done or not self.started_solving: return

        r, c = self.solve_current
        if (r, c) == self.solve_target:
            self.solve_done = True
            self.status = "Solved!"
            return

        # Find valid next moves (no wall and not visited/dead-end)
        moves = []
        # North
        if r < self.R and self.north_walls[r][c] == 0 and (r+1, c) not in self.visited_solve and (r+1, c) not in self.dead_ends:
            moves.append((r+1, c))
        # South
        if r > 1 and self.north_walls[r-1][c] == 0 and (r-1, c) not in self.visited_solve and (r-1, c) not in self.dead_ends:
            moves.append((r-1, c))
        # East
        if c < self.C and self.east_walls[r][c] == 0 and (r, c+1) not in self.visited_solve and (r, c+1) not in self.dead_ends:
            moves.append((r, c+1))
        # West
        if c > 1 and self.east_walls[r][c-1] == 0 and (r, c-1) not in self.visited_solve and (r, c-1) not in self.dead_ends:
            moves.append((r, c-1))

        if moves:
            next_cell = random.choice(moves)
            self.solve_stack.append(next_cell)
            self.visited_solve.add(next_cell)
            self.solve_current = next_cell
        elif self.solve_stack:
            # Dead end: backtrack
            self.dead_ends.add(self.solve_current)
            self.solve_stack.pop()
            if self.solve_stack:
                self.solve_current = self.solve_stack[-1]
        else:
            self.solve_done = True
            self.status = "No path found!"

    def render(self, width, height):
        """Render walls and dots."""
        sx = width / (self.C + 2)
        sy = height / (self.R + 2)
        ox, oy = sx, sy

        # Draw Walls
        glColor3f(0, 0, 0)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        # North walls
        for r in range(self.R + 1):
            for c in range(1, self.C + 1):
                if self.north_walls[r][c]:
                    glVertex2f(ox + (c-1)*sx, oy + r*sy)
                    glVertex2f(ox + c*sx, oy + r*sy)
        # East walls
        for r in range(1, self.R + 1):
            for c in range(self.C + 1):
                if self.east_walls[r][c]:
                    glVertex2f(ox + c*sx, oy + (r-1)*sy)
                    glVertex2f(ox + c*sx, oy + r*sy)
        glEnd()

        # Dots
        glPointSize(8.0)
        glBegin(GL_POINTS)
        if not self.gen_done:
            glColor3f(0, 1, 0) # Green for generation cursor
            glVertex2f(ox + (self.gen_current[1]-0.5)*sx, oy + (self.gen_current[0]-0.5)*sy)
        
        if self.started_solving:
            # Dead ends in Blue
            glColor3f(0, 0, 1)
            for dr, dc in self.dead_ends:
                glVertex2f(ox + (dc-0.5)*sx, oy + (dr-0.5)*sy)
            # Current path in Red
            glColor3f(1, 0, 0)
            for sr, sc in self.solve_stack:
                glVertex2f(ox + (sc-0.5)*sx, oy + (sr-0.5)*sy)
        glEnd()

def main():
    # Configuration
    ROWS = 20
    COLS = 20
    CELL_SIZE = 30
    PADDING = 2 # 2 cells worth of padding
    
    # Calculate window size based on 30px per square plus padding
    window_width = (COLS + PADDING) * CELL_SIZE
    window_height = (ROWS + PADDING) * CELL_SIZE
    
    pygame.init()
    d_size = (window_width, window_height)
    pygame.display.set_mode(d_size, DOUBLEBUF | OPENGL)
    
    glClearColor(1, 1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, d_size[0], 0, d_size[1])

    maze = Maze(ROWS, COLS)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT: running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE and maze.gen_done:
                    maze.started_solving = True
                    maze.status = "Solving..."
                if event.key == K_r:
                    maze = Maze(ROWS, COLS)

        if not maze.gen_done:
            maze.generate_step()
        elif maze.started_solving and not maze.solve_done:
            # Automatic stepping for solver
            maze.solve_step()

        # Update window title with status
        pygame.display.set_caption(f"Maze - {maze.status}")
        
        glClear(GL_COLOR_BUFFER_BIT)
        maze.render(d_size[0], d_size[1])
        pygame.display.flip()
        
        # Adjust speed: Generation is fast, Solving is slightly slower for visibility
        if not maze.gen_done:
            clock.tick(240) 
        else:
            clock.tick(60) 

    pygame.quit()

if __name__ == "__main__":
    main()

