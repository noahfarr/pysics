# Pysics

This project is a 2d particle simulation implemented in Python, featuring optimized collision detection and resolution. The simulation includes rendering capabilities to visualize the particles and their interactions.

## Features

- Particle generation with random initial positions and velocities.
- Gravity and wall constraints.
- Collision detection using spatial partitioning for efficiency.
- Collision resolution with impulse-based physics.
- Rendering support to visualize the simulation.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/noahfarr/pysics.git
    cd pysics
    ```

2. Install the dependencies:
    ```sh
    poetry install
    ```

3. Activate the virtual environment:
    ```sh
    poetry shell
    ```

## Usage

To run the simulation, you need to have a renderer implemented. This project already has a `RaylibRenderer` implemented.

1. Ensure you have the renderer set up and import it in the simulation script.

2. Create a script to run the simulation:
    ```python
    from pysics.render import RaylibRenderer
    from simulation import Simulation

    if __name__ == "__main__":
        renderer = RaylibRenderer((800, 600))  # Set the window size as needed
        sim = Simulation(n_particles=100, dt=0.01, renderer=renderer)
        sim.simulate(total_timesteps=1000, render=True)
    ```

All of these options can be set in the config.py file.

3. Run the script:
    ```sh
    python main.py
    ```

## Project Structure

- `simulation.py`: Contains the `Simulation` class and related logic.
- `particle.py`: Contains the `Particle` class with physics properties and methods.
- `render.py`: Contains the `Renderer` and `RaylibRenderer` classes for visualizing the simulation.
- `config.py`: Contains a dataclass to configure the parameters of the simulation.
- `pyproject.toml`: Configuration file for `poetry`, listing dependencies and project metadata.

## Optimization Techniques

1. **Spatial Partitioning**: Efficiently detects potential collisions by dividing the simulation space into a grid.
2. **Vectorized Operations**: Utilizes NumPy for efficient mathematical operations.
3. **Reduced Function Call Overheads**: Simplifies and inlines frequently called functions.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
