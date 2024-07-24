import tyro

from config import Config

from pysics.simulation import Simulation
from pysics.render import Renderer, RaylibRenderer


def main(config: Config):

    renderer: Renderer = RaylibRenderer(size=config.size, target_fps=config.target_fps)

    simulation = Simulation(
        n_particles=config.n_particles,
        gravity=config.gravity,
        dt=config.dt,
        renderer=renderer,
        WALL_DAMP=config.wall_damp,
        RESTITUTION=config.restitution,
    )
    simulation.simulate(total_timesteps=config.total_timesteps, render=config.render)


if __name__ == "__main__":
    config = tyro.cli(Config)
    main(config)
