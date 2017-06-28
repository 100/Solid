from random import choice, randint, random
from string import ascii_lowercase
from Solid.EvolutionaryAlgorithm import EvolutionaryAlgorithm


class Algorithm(EvolutionaryAlgorithm):
    """
    Tries to get a randomly-generated string to match string "clout"
    """
    def _initial_population(self):
        return list(''.join([choice(ascii_lowercase) for _ in range(5)]) for _ in range(50))

    def _fitness(self, member):
        return float(sum(member[i] == "clout"[i] for i in range(5)))

    def _crossover(self, parent1, parent2):
        partition = randint(0, len(self.population[0]) - 1)
        return parent1[0:partition] + parent2[partition:]

    def _mutate(self, member):
        if self.mutation_rate >= random():
            member = list(member)
            member[randint(0, 4)] = choice(ascii_lowercase)
            member = ''.join(member)
        return member


def test_algorithm():
    algorithm = Algorithm(.5, .7, 500, max_fitness=None)
    algorithm.run()
