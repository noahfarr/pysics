from dataclasses import dataclass


@dataclass
class Config:
    n_particles: int = 50
    total_timesteps: int = 1000
    dt: float = 0.01
    gravity: float = 9.81
    size: tuple[int, int] = (1200, 800)
    target_fps: int = 60
    render: bool = False
    wall_damp: float = 0.95
    restitution: float = 0.95
