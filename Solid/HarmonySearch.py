from abc import ABCMeta, abstractmethod
from random import choice, random, uniform
from numpy import argmax, argmin


class HarmonySearch:
    """
    Conducts harmony search
    """
    __metaclass__ = ABCMeta

    cur_steps = None

    hms = None
    hmcr = None
    par = None
    fw = None

    memory = None
    scores = None
    best = None

    max_steps = None
    max_score = None

    def __init__(self, hms, hmcr, par, fw, max_steps, max_score=None):
        """

        :param hms: harmony memory size
        :param hmcr: harmony memory considering rate
        :param par: pitch adjustment rate
        :param fw: fret width
        :param max_steps: maximum number of steps to run algorithm for
        :param max_score: objective function value to stop algorithm once reached
        """
        if isinstance(hms, int) and hms > 0:
            self.hms = hms
        else:
            raise TypeError('Harmony memory size must be a positive integer')

        if isinstance(hmcr, float) and 0 <= hmcr <= 1:
            self.hmcr = hmcr
        else:
            raise TypeError('Harmony memory considering rate must be a float between 0 and 1')

        if isinstance(par, float) and 0 <= par <= 1:
            self.par = par
        else:
            raise TypeError('Pitch adjustment rate must be a float between 0 and 1')

        if isinstance(fw, (int, float)):
            self.fw = float(fw)
        else:
            raise TypeError('Fret width must be a numeric type')

        if isinstance(max_steps, int) and max_steps > 0:
            self.max_steps = max_steps
        else:
            raise TypeError('Max steps must be a positive integer')

        if max_score is not None:
            if isinstance(max_score, (int, float)):
                self.max_score = max_score
            else:
                raise TypeError('Max score must be a numeric type')

    def __str__(self):
        return ('HARMONY SEARCH: \n' +
                'CURRENT STEPS: %d \n' +
                'BEST SCORE: %f \n' +
                'BEST MEMBER: %s \n\n') % \
               (self.cur_steps, self._score(self.best), str(self.best))

    def __repr__(self):
        return self.__str__()

    def _clear(self):
        """
        Resets the variables that are altered on a per-run basis of the algorithm

        :return: None
        """
        self.cur_steps = 0
        self.memory = list([self._random_harmony() for _ in range(self.hms)])
        self.scores = None

    @abstractmethod
    def _random_harmony(self):
        """
        Generates a random harmony, represented as a list of floats

        :return: list of harmonies
        """
        pass

    @abstractmethod
    def _score(self, harmony):
        """
        Returns score of a harmony

        :param harmony: a harmony
        :return: score of harmony
        """
        pass

    def _score_all(self):
        """
        Finds score of all current harmonies in memory

        :return: None
        """
        self.scores = list([self._score(x) for x in self.memory])

    def _worst_score(self):
        """
        Returns index of worst harmony in memory

        :return: index of worst harmony in memory
        """
        return argmin(self.scores)

    def _best_score(self):
        """
        Returns index of best harmony in memory

        :return: index of best harmony in memory
        """
        return argmax(self.scores)

    def run(self, verbose=True):
        """
        Conducts harmony search

        :param verbose: indicates whether or not to print progress regularly
        :return: best state and objective function value of best state
        """
        self._clear()
        self._score_all()
        for i in range(self.max_steps):
            self.cur_steps += 1

            if ((i + 1) % 100 == 0) and verbose:
                print self

            self._score_all()

            selected = [0.] * len(self.memory[0])
            for i in range(len(selected)):
                if self.hmcr >= random():
                    selected_component = choice(self.memory)[i]
                    if self.par >= random():
                        selected_component += uniform(-1, 1) * self.fw
                else:
                    selected_component = self._random_harmony()[i]
                selected[i] = selected_component

            if self._score(selected) > self._score(self.memory[self._worst_score()]):
                self.memory[self._worst_score()] = selected
                self.scores[self._worst_score()] = self._score(selected)

            self.best = self.memory[self._best_score()]

            if self.max_score is not None and self._score(self.best) > self.max_score:
                print "TERMINATING - REACHED MAXIMUM SCORE"
                return self.best, self._score(self.best)
        print "TERMINATING - REACHED MAXIMUM STEPS"
        return self.best, self._score(self.best)