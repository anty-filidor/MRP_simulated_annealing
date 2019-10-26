from datasets import Datasets
from simulated_annealing import SimulatedAnnealing

path = '/Users/michal/PycharmProjects/MRP/datasets/*.tsp'
data = Datasets(path)

# name = 'ali535'
# name = 'berlin11_modified'
name = 'berlin52'
# name = 'fl417'
# name = 'gr666'
# name = 'kroA100'
# name = 'kroA150'
# name = 'nrw1379'
# name = 'pr2392'


SA = SimulatedAnnealing(data, name)
stats = SA(t_start=3000, t_min=10)

for iterator, log in enumerate(stats.items()):

    print('ITERATION {}'.format(iterator))
    print('\t\tbest distance - {}'.format(log[0]))
    print('\t\tbest route - {}'.format(log[1]))
    print('\n')
