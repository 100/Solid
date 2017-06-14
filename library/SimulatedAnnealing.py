from abc import ABCMeta, abstractmethod
from copy import deepcopy
from math import exp
from random import random


class SimulatedAnnealing:
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
        self.current_temp *= schedule_constant

    def _linear(self, schedule_constant):
        self.current_temp -= schedule_constant

    def _get_schedule(self, schedule_str, schedule_constant):
        if schedule_str == 'exponential':
            return self._exponential(schedule_constant)
        elif schedule_str == 'linear':
            return self._linear(schedule_constant)
        else:
            raise ValueError('Annealing schedule must be either "exponential" or "linear"')

    def __init__(self, initial_state, max_steps, temp_begin, schedule_constant,
                 min_energy=None, schedule_str='exponential'):
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

        self.adjust_temp = self._get_schedule(schedule_str, schedule_constant)

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
        self.cur_steps = 0
        self.current_state = None
        self.best_state = None
        self.current_energy = None
        self.best_energy = None

    @abstractmethod
    def _neighbor(self):
        pass

    @abstractmethod
    def _energy(self, state):
        pass

    def _accept_neighbor(self, neighbor):
        p = exp(self._energy(self.current_state) - self._energy(neighbor)) / self.current_temp
        return True if p >= 1 else p >= random()

    def anneal(self, verbose=True):
        self._clear()
        self.current_state = self.initial_state
        self.current_temp = self.start_temp
        for i in range(self.max_steps):
            self.cur_steps += 1

            if (i % 100 == 0) and verbose:
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

            self.current_temp = self.adjust_temp()
        print "TERMINATING - REACHED MAXIMUM STEPS"
        return self.best_state, self.best_energy