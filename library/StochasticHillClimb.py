from abc import ABCMeta, abstractmethod
from copy import deepcopy
from math import exp
from random import random


class StochasticHillClimb:
    """
    Conducts stochastic hill climb
    """
    __metaclass__ = ABCMeta

    initial_state = None
    current_state = None
    best_state = None

    cur_steps = 0
    max_steps = None

    best_objective = None
    max_objective = None

    temp = None

    def __init__(self, initial_state, temp, max_steps, max_objective=None):
        """
        
        :param initial_state: initial state of hill climbing
        :param max_steps: maximum steps to run hill climbing for
        :param temp: temperature in probabilistic acceptance of transition
        :param max_objective: objective function to stop algorithm once reached
        """
        self.initial_state = initial_state

        if isinstance(max_steps, int) and max_steps > 0:
            self.max_steps = max_steps
        else:
            raise ValueError('Max steps must be a positive integer')

        if max_objective is not None:
            if isinstance(max_objective, (float, int)):
                self.max_objective = float(max_objective)
            else:
                raise ValueError('Maximum objective must be a numeric type')

        if isinstance(temp, (float, int)):
            self.temp = float(temp)
        else:
            raise ValueError('Temperature must be a numeric type')

    def __str__(self):
        return ('STOCHASTIC HILL CLIMB: \n' +
                'CURRENT STEPS: %d \n' +
                'BEST OBJECTIVE: %f \n' +
                'BEST STATE: %s \n\n') % \
               (self.cur_steps, self.best_objective, str(self.best_state))

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
        self.best_objective = None

    @abstractmethod
    def _neighbor(self):
        """
        Returns a random member of the neighbor of the current state

        :return: a random neighbor, given access to self.current_state
        """
        pass

    @abstractmethod
    def _objective(self, state):
        """
        Evaluates a given state

        :param state: a state
        :return: objective function value of state
        """
        pass

    def _accept_neighbor(self, neighbor):
        """
        Probabilistically determines whether or not to accept a transition to a neighbor

        :param neighbor: a state
        :return: boolean indicating whether or not transition was accepted
        """
        try:
            p = 1. / (1 + (exp((self._objective(self.current_state) - self._objective(neighbor)) / self.temp)))
        except OverflowError:
            return True
        return True if p >= 1 else p >= random()

    def run(self, verbose=True):
        """
        Conducts hill climb

        :param verbose: indicates whether or not to print progress regularly
        :return: best state and best objective function value
        """
        self._clear()
        self.current_state = self.initial_state
        for i in range(self.max_steps):
            self.cur_steps += 1

            if ((i + 1) % 100 == 0) and verbose:
                print self

            neighbor = self._neighbor()

            if self._accept_neighbor(neighbor):
                self.current_state = neighbor

            if self._objective(self.current_state) > self.best_objective:
                self.best_objective = self._objective(self.current_state)
                self.best_state = deepcopy(self.current_state)

            if self.max_objective is not None and self.best_objective > self.max_objective:
                print "TERMINATING - REACHED MAXIMUM OBJECTIVE"
                return self.best_state, self.best_objective
        print "TERMINATING - REACHED MAXIMUM STEPS"
        return self.best_state, self.best_objective