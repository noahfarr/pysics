from abc import ABC, abstractmethod
import pyray as pr

from pysics.particle import Particle


class Renderer(ABC):

    size: tuple[int, int]

    @abstractmethod
    def render(self, particles: list[Particle]):
        pass

    @abstractmethod
    def close(self):
        pass


class RaylibRenderer(Renderer):

    def __init__(
        self, size: tuple[int, int] | None = None, target_fps: int | None = None
    ) -> None:
        self.size = size or (800, 450)
        self.target_fps = target_fps or 60
        pr.init_window(*self.size, "Pysics")
        pr.set_target_fps(self.target_fps)

    def render(self, particles: list[Particle]):
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        # Draw each circle from the list
        for body in particles:
            x = int(body.position[0])
            y = self.size[1] - int((body.position[1]))
            radius = int(body.radius)
            pr.draw_circle(x, y, radius, pr.DARKBLUE)

        # End drawing
        pr.end_drawing()

    def close(self):
        pr.close_window()
