from abc import ABCMeta, abstractmethod
from random import random
from numpy import apply_along_axis, argmin, array, copy, dot, fill_diagonal, zeros
from numpy.random import uniform


class ParticleSwarm:
    __metaclass__ = ABCMeta

    swarm_size = None
    member_size = None
    lower_bound = None
    upper_bound = None

    pos = None
    vel = None
    scores = None
    best = None
    global_best = None

    c1 = None
    c2 = None
    c3 = None

    cur_steps = None
    max_steps = None
    min_objective = None

    def __init__(self, swarm_size, member_size, lower_bound, upper_bound, c1, c2, c3,
                 max_steps, min_objective=None):
        if isinstance(swarm_size, int):
            if swarm_size > 0:
                self.swarm_size = swarm_size
            else:
                raise ValueError('Swarm size must be a positive integer')
        else:
            raise ValueError('Swarm size must be a positive integer')

        if isinstance(member_size, int):
            if member_size > 0:
                self.member_size = member_size
            else:
                raise ValueError('Member size must be a positive integer')
        else:
            raise ValueError('Member size must be a positive integer')

        if isinstance(lower_bound, (int, float)):
            self.lower_bound = float(lower_bound)
        else:
            raise ValueError()

        if isinstance(upper_bound, (int, float)):
            self.upper_bound = float(upper_bound)
        else:
            raise ValueError()

        self.pos = uniform(lower_bound, upper_bound, size=(swarm_size, member_size))

        self.vel = uniform(upper_bound - lower_bound, lower_bound - upper_bound, size=(swarm_size, member_size))

        self.best = copy(self.pos)

        if isinstance(c1, (int, float)) and isinstance(c2, (int, float)) and isinstance(c3, (int, float)):
            self.c1 = float(c1)
            self.c2 = float(c2)
            self.c3 = float(c3)
        else:
            raise ValueError()

        if isinstance(max_steps, int):
            self.max_steps = max_steps
        else:
            raise ValueError()

        if min_objective is not None:
            if isinstance(min_objective, (int, float)):
                self.min_objective = float(min_objective)
            else:
                raise ValueError()

    def __str__(self):
        return ('PARTICLE SWARM: \n' +
                'CURRENT STEPS: %d \n' +
                'BEST FITNESS: %f \n' +
                'BEST MEMBER: %s \n\n') % \
               (self.cur_steps, self._score(self.global_best[0]), str(self.global_best[0]))

    def __repr__(self):
        return self.__str__()

    def _clear(self):
        self.pos = uniform(self.lower_bound, self.upper_bound, size=(self.swarm_size, self.member_size))
        self.vel = uniform(self.upper_bound - self.lower_bound, self.lower_bound - self.upper_bound, size=(self.swarm_size, self.member_size))
        self.scores = self._score(self.pos)
        self.best = copy(self.pos)
        self.cur_steps = 0

    @abstractmethod
    def _objective(self, member):
        pass

    def _score(self, pos):
        return apply_along_axis(self._objective, 1, pos)

    def _best(self, old, new):
        old_score = self._score(old)
        new_score = self._score(new)
        best = []
        for i in range(len(old_score)):
            if old_score > new_score:
                best.append(old[i])
            else:
                best.append(new[i])
        self.best = array(best)

    def _global_best(self):
        if min(self.scores) < self.global_best[0][0]:
            self.global_best = array([self.pos[argmin(self.scores)],] * self.swarm_size)

    def swarm(self, verbose=True):
        self._clear()
        for i in range(self.max_steps):
            self.cur_steps += 1

            if (i % 100 == 0) and verbose:
                print self

            u1 = fill_diagonal(zeros((self.swarm_size, self.swarm_size)), random())
            u2 = fill_diagonal(zeros((self.swarm_size, self.swarm_size), random()))

            vel_new = (self.c1 * self.vel) + \
                      (self.c2 * dot(u1, (self.best - self.pos))) + \
                      (self.c3 * dot(u2, (self.global_best - self.pos)))

            pos_new = self.pos + vel_new

            self._best(self.pos, pos_new)
            self.pos = pos_new
            self.scores = self._score(self.pos)
            self._global_best()

            if self._score(self.global_best[0]) < self.min_objective:
                print "TERMINATING - REACHED MINIMUM OBJECTIVE"
                return self.global_best[0], self._score(self.global_best[0])
        print "TERMINATING - REACHED MAXIMUM STEPS"
        return self.global_best[0], self._score(self.global_best[0])
