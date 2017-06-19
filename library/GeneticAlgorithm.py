from abc import ABCMeta, abstractmethod
from copy import deepcopy
from random import randint, random, shuffle


class GeneticAlgorithm:
    """
    Conducts genetic algorithm
    """
    __metaclass__ = ABCMeta

    population = None
    fitnesses = None

    crossover_rate = None

    mutation_rate = None

    cur_steps = None
    best_fitness = None
    best_member = None

    max_steps = None
    max_fitness = None

    def __init__(self, crossover_rate, mutation_rate, max_steps, max_fitness=None):
        """

        :param crossover_rate: probability of crossover
        :param mutation_rate: probability of mutation
        :param max_steps: maximum steps to run genetic algorithm for
        :param max_fitness: fitness value to stop algorithm once reached
        """
        if isinstance(crossover_rate, float):
            if crossover_rate >= 0 and crossover_rate <= 1:
                self.crossover_rate = crossover_rate
            else:
                raise ValueError('Crossover rate must be a float between 0 and 1')
        else:
            raise ValueError('Crossover rate must be a float between 0 and 1')

        if isinstance(mutation_rate, float):
            if mutation_rate >= 0 and mutation_rate <= 1:
                self.mutation_rate = mutation_rate
            else:
                raise ValueError('Mutation rate must be a float between 0 and 1')
        else:
            raise ValueError('Mutation rate must be a float between 0 and 1')

        if isinstance(max_steps, int) and max_steps > 0:
            self.max_steps = max_steps
        else:
            raise ValueError('Maximum steps must be a positive integer')

        if max_fitness is not None:
            if isinstance(max_fitness, (int, float)):
                self.max_fitness = float(max_fitness)
            else:
                raise ValueError('Maximum fitness must be a numeric type')

    def __str__(self):
        return ('GENETIC ALGORITHM: \n' +
                'CURRENT STEPS: %d \n' +
                'BEST FITNESS: %f \n' +
                'BEST MEMBER: %s \n\n') % \
               (self.cur_steps, self.best_fitness, str(self.best_member))

    def __repr__(self):
        return self.__str__()

    def _clear(self):
        """
        Resets the variables that are altered on a per-run basis of the algorithm

        :return: None
        """
        self.cur_steps = 0
        self.population = None
        self.fitnesses = None
        self.best_member = None
        self.best_fitness = None

    @abstractmethod
    def _initial_population(self):
        """
        Generates initial population -
        members must be represented by a list of binary-values integers

        :return: list of members of population
        """
        pass

    @abstractmethod
    def _fitness(self, member):
        """
        Evaluates fitness of a given member

        :param member: a member
        :return: fitness of member
        """
        pass

    def _populate_fitness(self):
        """
        Calculates fitness of all members of current population

        :return: None
        """
        self.fitnesses = list([self._fitness(x) for x in self.population])

    def _most_fit(self):
        """
        Finds most fit member of current population

        :return: most fit member and most fit member's fitness
        """
        best_idx = 0
        cur_idx = 0
        for x in self.fitnesses:
            if x > self.fitnesses[best_idx]:
                best_idx = cur_idx
            cur_idx += 1
        return self.population[best_idx], self.fitnesses[best_idx]

    def _select_n(self, n):
        """
        Probabilistically selects n members from current population using
        roulette-wheel selection

        :param n: number of members to select
        :return: n members
        """
        shuffle(self.population)
        total_fitness = sum(self.fitnesses)
        if total_fitness != 0:
            probs = list([self._fitness(x) / total_fitness for x in self.population])
        else:
            return self.population[0:n]
        res = []
        for _ in range(n):
            r = random()
            sum_ = 0
            for i, x in enumerate(probs):
                sum_ += probs[i]
                if r <= sum_:
                    res.append(deepcopy(self.population[i]))
                    break
        return res

    def _crossover(self, parent1, parent2):
        """
        Creates new member of population by combining two parent members

        :param parent1: a member
        :param parent2: a member
        :return: member made by combining elements of both parents
        """
        partition = randint(0, len(self.population[0]) - 1)
        return parent1[0:partition] + parent2[partition:]

    def _mutate(self, member):
        """
        Randomly mutates a member

        :param member: a member
        :return: mutated member
        """
        if self.mutation_rate >= random():
            idx = randint(0, len(member) - 1)
            member[idx] = 1 if member[idx] == 0 else 1
        return member

    def run(self, verbose=True):
        """
        Conducts genetic algorithm

        :param verbose: indicates whether or not to print progress regularly
        :return: best state and best objective function value
        """
        self._clear()
        self.population = self._initial_population()
        self._populate_fitness()
        self.best_member, self.best_fitness = self._most_fit()
        num_copy = max(int((1 - self.crossover_rate) * len(self.population)), 2)
        num_crossover = len(self.population) - num_copy
        for i in range(self.max_steps):
            self.cur_steps += 1

            if ((i + 1) % 100 == 0) and verbose:
                print self

            self.population = self._select_n(num_copy)
            self._populate_fitness()

            parents = self._select_n(2)
            for _ in range(num_crossover):
                self.population.append(self._crossover(*parents))

            self.population = list([self._mutate(x) for x in self.population])
            self._populate_fitness()

            best_member, best_fitness = self._most_fit()
            if best_fitness > self.best_fitness:
                self.best_fitness = best_fitness
                self.best_member = deepcopy(best_member)

            if self.max_fitness is not None and self.best_fitness >= self.max_fitness:
                print "TERMINATING - REACHED MAXIMUM FITNESS"
                return self.best_member, self.best_fitness
        print "TERMINATING - REACHED MAXIMUM STEPS"
        return self.best_member, self.best_fitness
