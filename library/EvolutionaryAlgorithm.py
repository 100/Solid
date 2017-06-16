from abc import ABCMeta, abstractmethod
from copy import deepcopy
from random import randint, random, shuffle


class EvolutionaryAlgorithm:
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
        return ('EVOLUTIONARY ALGORITHM: \n' +
                'CURRENT STEPS: %d \n' +
                'BEST FITNESS: %f \n' +
                'BEST MEMBER: %s \n\n') % \
               (self.cur_steps, self.best_fitness, str(self.best_member))

    def __repr__(self):
        return self.__str__()

    def _clear(self):
        self.cur_steps = 0
        self.population = None
        self.fitnesses = None
        self.best_member = None
        self.best_fitness = None

    @abstractmethod
    def _initial_population(self):
        pass

    @abstractmethod
    def _fitness(self, member):
        pass

    def _populate_fitness(self):
        self.fitnesses = list([self._fitness(x) for x in self.population])

    def _most_fit(self):
        best_idx = 0
        cur_idx = 0
        for x in self.fitnesses:
            if x > self.fitnesses[best_idx]:
                best_idx = cur_idx
            cur_idx += 1
        return self.population[best_idx], self.fitnesses[best_idx]

    def _select_n(self, n):
        shuffle(self.population)
        total_fitness = sum(self.fitnesses)
        probs = list([self._fitness(x) / total_fitness for x in self.population])
        res = []
        for _ in probs:
            r = random()
            sum = 0
            for i, x in enumerate(probs):
                sum += probs[i]
                if r < sum:
                    res.add(deepcopy(self.population[i]))
        return res

    @abstractmethod
    def _crossover(self, parent1, parent2):
        pass

    @abstractmethod
    def _mutate(self, member):
        pass

    def evolutionary_algorithm(self, verbose=True):
        num_copy = int((1 - self.crossover_rate) * len(self.population))
        num_crossover = len(self.population) - num_copy
        self._clear()
        self.population = self._initial_population()
        for i in range(self.max_steps):
            self.cur_steps += 1

            if (i % 100 == 0) and verbose:
                print self

            self._populate_fitness()
            self.population = self._select_n(num_copy)

            parents = self._select_n(2)
            for _ in range(num_crossover):
                self.population.append(self._crossover(*parents))

            self.population = list([self.mutate(x) for x in self.population])
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
