import operator
import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt
from tqdm import tqdm


class SimulatedAnnealing:
    def __init__(self, datasets, name):
        self.datasets = datasets
        self.name = name

    def _generate_individual(self):
        return self.datasets.get_permutation(self.name)

    def _rank_individual(self, individual):
        return self.datasets.distance_permutation(self.name, individual)

    @staticmethod
    def _mutate(individual):
        # copy individual
        new_individual = list(individual[:-1])
        # select indices to swap
        index_a = int(random.random() * len(new_individual))
        index_b = int(random.random() * len(new_individual))
        # be sure that index_a is not same as index_b
        while index_a == index_b:
            index_b = int(random.random() * len(new_individual))

        # swap values
        temp = new_individual[index_a]
        new_individual[index_a] = new_individual[index_b]
        new_individual[index_b] = temp

        # append first gene to end of the list
        new_individual.append(new_individual[0])

        return new_individual

    def plot_fancy_figure(self, x, y1, y2, label_x='x', label_y1='y1', label_y2='y2'):
        fig, ax1 = plt.subplots()
        ax1.set_xlabel(label_x)
        ax1.set_ylabel(label_y1, color='red')
        ax1.plot(x, y1, '-', color='red')
        ax1.tick_params(axis='y', labelcolor='red')

        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel(label_y2, color='blue')  # we already handled the x-label with ax1
        ax2.plot(x, y2, '-', color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')

        plt.grid(linewidth='0')
        fig.tight_layout()
        plt.title('Best distance in {}: {}'.format(self.name, min(y1).round(2)))
        plt.show()

    def __call__(self, t_start, t_min):
        #  Initialise lists to keep best results in each epoch
        iteration_distances = []
        iteration_routes = []
        iteration_temperatures = []

        #  Initialise individual
        individual = self._generate_individual()
        individual_distance = self._rank_individual(individual)

        #  Main loop
        t = t_start
        while t >= t_min:

            new_individual = self._mutate(individual)
            new_individual_distance = self._rank_individual(new_individual)

            if new_individual_distance < individual_distance:
                individual = new_individual
                individual_distance = new_individual_distance

            elif random.random() < np.exp(- (new_individual_distance - individual_distance) / t):
                individual = new_individual
                individual_distance = new_individual_distance

            t = 0.99 * t

            #  Update stats lists
            iteration_routes.append(individual)
            iteration_distances.append(individual_distance)
            iteration_temperatures.append(t)

        self.plot_fancy_figure(x=np.arange(0, len(iteration_temperatures)), y1=iteration_distances,
                               y2=iteration_temperatures, label_x='iteration', label_y1='distance',
                               label_y2='temperature')

        return dict(zip(iteration_distances, iteration_routes))

