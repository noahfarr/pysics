from abc import ABC, abstractmethod

class Renderer(ABC):
    @abstractmethod
    def render(self, bodies):
        pass

    @abstractmethod
    def draw_rectangle(self, body):
        pass

    @abstractmethod
    def draw_circle(self, body):
        pass

    @abstractmethod
    def draw_polygon(self, body):
        pass
