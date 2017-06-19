from abc import ABCMeta, abstractmethod
from copy import deepcopy
from math import exp
from random import random


class SimulatedAnnealing:
    """
    Conducts simulated annealing algorithm
    """
    __metaclass__ = ABCMeta

    initial_state = None
    current_state = None
    best_state = None

    cur_steps = 0
    max_steps = None

    current_energy = None
    best_energy = None
    min_energy = None

    start_temp = None
    current_temp = None
    adjust_temp = None

    def _exponential(self, schedule_constant):
        def f():
            self.current_temp *= schedule_constant
        return f

    def _linear(self, schedule_constant):
        def f():
            self.current_temp -= schedule_constant
        return f

    def _get_schedule(self, schedule_str, schedule_constant):
        if schedule_str == 'exponential':
            return self._exponential(schedule_constant)
        elif schedule_str == 'linear':
            return self._linear(schedule_constant)
        else:
            raise ValueError('Annealing schedule must be either "exponential" or "linear"')

    def __init__(self, initial_state, temp_begin, schedule_constant, max_steps,
                 min_energy=None, schedule='exponential'):
        """

        :param initial_state: initial state of annealing algorithm
        :param max_steps: maximum number of iterations to conduct annealing for
        :param temp_begin: beginning temperature
        :param schedule_constant: constant value in annealing schedule function
        :param min_energy: energy value to stop algorithm once reached
        :param schedule: 'exponential' or 'linear' annealing schedule
        """
        self.initial_state = initial_state

        if isinstance(max_steps, int) and max_steps > 0:
            self.max_steps = max_steps
        else:
            raise ValueError('Max steps must be a positive integer')

        if min_energy is not None:
            if isinstance(min_energy, (float, int)):
                self.min_energy = float(min_energy)
            else:
                raise ValueError('Minimum energy must be a numeric type')

        if isinstance(temp_begin, (float, int)):
            self.start_temp = float(temp_begin)
        else:
            raise ValueError('Starting temperature must be a numeric type')

        self.adjust_temp = self._get_schedule(schedule, schedule_constant)

    def __str__(self):
        return ('SIMULATED ANNEALING: \n' +
                'CURRENT STEPS: %d \n' +
                'CURRENT TEMPERATURE: %f \n' +
                'BEST ENERGY: %f \n' +
                'BEST STATE: %s \n\n') % \
               (self.cur_steps, self.current_temp, self.best_energy, str(self.best_state))

    def __repr__(self):
        return self.__str__()

    def _clear(self):
        """
        Resets the variables that are altered on a per-run basis of the algorithm

        :return: None
        """
        self.cur_steps = 0
        self.current_state = None
        self.best_state = None
        self.current_energy = None
        self.best_energy = None

    @abstractmethod
    def _neighbor(self):
        """
        Returns a random member of the neighbor of the current state

        :return: a random neighbor, given access to self.current_state
        """
        pass

    @abstractmethod
    def _energy(self, state):
        """
        Finds the energy of a given state

        :param state: a state
        :return: energy of state
        """
        pass

    def _accept_neighbor(self, neighbor):
        """
        Probabilistically determines whether or not to accept a transition to a neighbor

        :param neighbor: a state
        :return: boolean indicating whether or not transition is accepted
        """
        try:
            p = exp(-(self._energy(neighbor) - self._energy(self.current_state)) / self.current_temp)
        except OverflowError:
            return True
        return True if p >= 1 else p >= random()

    def run(self, verbose=True):
        """
        Conducts simulated annealing

        :param verbose: indicates whether or not to print progress regularly
        :return: best state and best energy
        """
        self._clear()
        self.current_state = self.initial_state
        self.current_temp = self.start_temp
        self.best_energy = self._energy(self.current_state)
        for i in range(self.max_steps):
            self.cur_steps += 1

            if ((i + 1) % 100 == 0) and verbose:
                print self

            neighbor = self._neighbor()

            if self._accept_neighbor(neighbor):
                self.current_state = neighbor
            self.current_energy = self._energy(self.current_state)

            if self.current_energy < self.best_energy:
                self.best_energy = self.current_energy
                self.best_state = deepcopy(self.current_state)

            if self.min_energy is not None and self.current_energy < self.min_energy:
                print "TERMINATING - REACHED MINIMUM ENERGY"
                return self.best_state, self.best_energy

            self.adjust_temp()
            if self.current_temp < 0.000001:
                print "TERMINATING - REACHED TEMPERATURE OF 0"
                return self.best_state, self.best_energy
        print "TERMINATING - REACHED MAXIMUM STEPS"
        return self.best_state, self.best_energy