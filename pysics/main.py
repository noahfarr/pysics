from world import World
from dynamics.bodies.rigid_body import RigidBody
from dynamics.bodies.shapes.rectangle import Rectangle
from dynamics.bodies.shapes.circle import Circle
from dynamics.bodies.shapes.polygon import Polygon
from collision.aabb import AABB
from rendering.pygame_renderer import PygameRenderer

import numpy as np



def aabb_factory(position, angle, shape):
    if isinstance(shape, Rectangle):
        half_width = shape.width / 2.0
        half_height = shape.height / 2.0
        corners = [
            [-half_width, -half_height],
            [half_width, -half_height],
            [half_width, half_height],
            [-half_width, half_height]
        ]
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        rotated_corners = np.dot(corners, rotation_matrix.T) + position
        min_corner = np.min(rotated_corners, axis=0)
        max_corner = np.max(rotated_corners, axis=0)
        return AABB(min_corner, max_corner)
    elif isinstance(shape, Circle):
        min_corner = position - np.array([shape.radius, shape.radius])
        max_corner = position + np.array([shape.radius, shape.radius])
        return AABB(min_corner, max_corner)
    elif isinstance(shape, Polygon):
        vertices = shape.vertices  # Assuming `vertices` is a NumPy array or similar
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        rotated_vertices = np.dot(vertices, rotation_matrix.T) + position
        min_coords = np.min(rotated_vertices, axis=0)
        max_coords = np.max(rotated_vertices, axis=0)
        return AABB(min_coords, max_coords)
    else:
        raise ValueError(f"Unsupported shape type: {type(shape)}")


if __name__ == "__main__":
    world = World(gravity=np.array([0, -9.81]))
    renderer = PygameRenderer(800, 600)
    world.set_renderer(renderer)
    #body1 = RigidBody(position=[0, 200], linear_velocity=[0, 0], angle=0, angular_velocity=1.0, shape=Rectangle(mass=1, width=100, height=100), bounding_volume_factory=aabb_factory)
    body2 = RigidBody(position=[0, 0], linear_velocity=[0, 0], angle=0, angular_velocity=10.0, shape=Polygon(1, 0.5, 6), bounding_volume_factory=aabb_factory)
    #world.add_body(body1)
    world.add_body(body2)
    for i in range(10000):
        world.update(0.01)
        
    
