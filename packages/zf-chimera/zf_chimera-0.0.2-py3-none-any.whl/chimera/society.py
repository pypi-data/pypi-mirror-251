from datetime import datetime
from random import randint
from random import shuffle
from random import uniform
from typing import List
from typing import Tuple
from uuid import uuid4

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

from .dists import age_dist
from .model import Person
from .model import Personality
from .utils import get_spiral_indices


def new_personality():
    return Personality(
        extroversion=uniform(0, 1),
        introversion=uniform(0, 1),
        sensing=uniform(0, 1),
        intuition=uniform(0, 1),
        thinking=uniform(0, 1),
        feeling=uniform(0, 1),
        judging=uniform(0, 1),
        perceiving=uniform(0, 1)
    )


def new_person(adopted=-1):
    adopted = uniform(0, 1) if adopted == -1 else adopted
    return Person(
        id=str(uuid4()),
        born=datetime(datetime.now().year - int(age_dist()), randint(1, 12), randint(1, 28)),
        personality=new_personality(),
        interests=[],
        adopted=adopted
    )


class Society:
    def __init__(self, args):
        self.args = args

        self.population = self.args.population
        self.n_rows = int(self.population ** 0.5)
        self.n_cols = self.n_rows
        self.n_agents = self.n_rows * self.n_cols

        self.grid = [[new_person(adopted=0) for _ in range(self.n_cols)] for _ in range(self.n_rows)]
        self.infected: List[Tuple[int, int]] = []

        if self.args.start == 'middle':
            r = self.n_rows // 2
            c = self.n_cols // 2

            self.grid[r][c].adopted = 1
            self.infected.append((r, c))
        elif self.args.start == 'random':
            while len(self.infected) < self.args.infected:
                r = randint(0, self.n_rows - 1)
                c = randint(0, self.n_cols - 1)

                if self.grid[r][c].adopted == 0:
                    self.grid[r][c].adopted = 1
                    self.infected.append((r, c))

        # self.plot()

    def simulate_v1(self, steps: int):
        """
        simulate_v1 simulates the diffusion of innovations in a society. Each infected members can infect
        """

        def step_v1(last_infected) -> List[Tuple[int, int]]:
            new_infected = []
            while len(last_infected) > 0:
                row, col = last_infected.pop()
                self.grid[row][col].adopted = 0.5  # Mark as done

                neighbors = self.get_neighbors(row, col, rounds=self.args.radius, count=self.args.spread)
                for neighbor in neighbors:
                    n_row, n_col = neighbor

                    if self.grid[n_row][n_col].adopted == 0:  # Infect the uninfected
                        if uniform(0, 1) < self.args.rate:
                            self.grid[n_row][n_col].adopted = 1
                            new_infected.append((n_row, n_col))

            return new_infected

        # Simulate
        grid_states = []
        for i in range(steps):
            self.infected = step_v1(self.infected)
            grid_states.append(self.copy_grid())

        # Plot
        fig, ax = plt.subplots(figsize=(5, 5))  # Create a figure for the animation
        ani = FuncAnimation(fig, self.update, frames=steps, interval=500, fargs=(grid_states, ax), repeat=False)
        writer = PillowWriter(fps=3, metadata=dict(artist='Me'), bitrate=1800)
        ani.save(f"./data/{str(uuid4())}.gif", writer=writer)
        plt.show()

    def simulate_v2(self, steps: int):
        """
        simulate_v2 simulates the diffusion of innovations in a society. Each infected members can infect
        """

        def step_v2(last_infected) -> List[Tuple[int, int]]:
            pass

    def get_neighbors(self, row, col, rounds, count):
        indices = get_spiral_indices(row, col, self.n_rows, self.n_cols, n=rounds)
        shuffle(indices)
        return indices[:count]

    def update(self, frame, grids, ax):
        ax.clear()  # Clear the previous image
        ax.imshow(grids[frame], cmap='viridis', interpolation='nearest', vmin=0.01)
        ax.set_xticks([])
        ax.set_yticks([])

    def plot(self):
        grid = self.copy_grid()
        fig, ax = plt.subplots(figsize=(5, 5))  # Set figure size as needed
        ax.imshow(grid, cmap='viridis', interpolation='nearest', vmin=0.01)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.show()

    def copy_grid(self) -> np.ndarray:
        return np.array([[self.grid[row][col].adopted for col in range(self.n_cols)] for row in range(self.n_rows)])
