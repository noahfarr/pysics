import pygame
import numpy as np

from .renderer import Renderer

# Pygame renderer
class PygameRenderer(Renderer):
    
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def render(self, bodies):
        self.screen.fill((255, 255, 255))
        for body in bodies:
            body.shape.draw(self, body)
        pygame.display.flip()
        self.clock.tick(30)

    def draw_rectangle(self, body):
        x, y = body.position
        x = int(x + self.width / 2)
        y = int(self.height / 2 - y)
        
        w, h = body.shape.width, body.shape.height

        # Create a new surface with the size of the rectangle
        rect_surface = pygame.Surface((w, h), pygame.SRCALPHA)

        # Draw the rectangle on that surface
        pygame.draw.rect(rect_surface, (255, 0, 0), (0, 0, w, h))

        # Rotate the rectangle surface
        angle_degrees = -body.angle * 180 / 3.14159  # Convert to degrees and negate to match Pygame's coordinate system
        rotated_rect_surface = pygame.transform.rotate(rect_surface, angle_degrees)

        # Find the new size and position after rotation
        new_rect = rotated_rect_surface.get_rect()
        new_rect.center = (x, y)

        # Blit the rotated surface onto the screen
        self.screen.blit(rotated_rect_surface, new_rect.topleft)

    def draw_circle(self, body):
        x, y = body.position
        x = int(x + self.width / 2)
        y = int(self.height / 2 - y )
        r = int(body.shape.radius)
        pygame.draw.circle(self.screen, (255, 0, 0), (x, y), r, 1)

    def draw_polygon(self, body):
        angle = body.angle  # in radians
        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)

        screen_vertices = []
        for vertex in body.shape.vertices:
            # Rotate the vertex (around the origin)
            x_rotated = vertex[0] * cos_angle - vertex[1] * sin_angle
            y_rotated = vertex[0] * sin_angle + vertex[1] * cos_angle

            # Translate to world coordinates by adding body's position
            x_world = x_rotated + body.position[0]
            y_world = y_rotated + body.position[1]

            # Transform to screen coordinates
            x_screen = int(x_world * 50 + self.width / 2)
            y_screen = int(self.height / 2 - y_world * 50)

            screen_vertices.append((x_screen, y_screen))

        pygame.draw.polygon(self.screen, (0, 0, 255), screen_vertices, 1)
