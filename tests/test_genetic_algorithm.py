from random import choice
from Solid.GeneticAlgorithm import GeneticAlgorithm


class Algorithm(GeneticAlgorithm):
    """
    Tries to get a randomly-generated string to match 000111
    """
    def _initial_population(self):
        return list(list([choice([0, 1]) for _ in range(6)]) for _ in range(50))

    def _fitness(self, member):
        return float(sum(member[i] == [0,0,0,1,1,1][i] for i in range(6)))


def test_algorithm():
    algorithm = Algorithm(.5, .7, 500, max_fitness=None)
    algorithm.run()
