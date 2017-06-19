from random import uniform
from Solid.SimulatedAnnealing import SimulatedAnnealing
from numpy import array


class Algorithm(SimulatedAnnealing):
    """
    Tries to get a randomly-generated list to match [.1, .2, .3, .2, .1]
    """
    def _neighbor(self):
        return list(array(self.current_state) + array([uniform(-.02, .02) for _ in range(5)]))

    def _energy(self, member):
        return sum(abs(member[i] - [.1, .2, .3, .2, .1][i]) if (member[i] > 0 or member[i] < 0) else 1 for i in range(5))


def test_algorithm():
    algorithm = Algorithm(list([uniform(0, 1) for _ in range(5)]), 5, .99, 5000)
    algorithm.run()
