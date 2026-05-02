import pygame
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# TODO: Write a function to the requested drawing here.


def main():
    pygame.init()
    display = (640, 480)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("PyOpenGL Window")
    
    # Set up OpenGL projection
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(2.0)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 640.0, 0.0, 480.0)

    clock = pygame.time.Clock()
    running = True
    
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # call the function here

        pygame.display.flip()     
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()