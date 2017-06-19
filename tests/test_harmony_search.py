from random import uniform
from Solid.HarmonySearch import HarmonySearch


class Algorithm(HarmonySearch):
    """
    Tries to get a randomly-generated list to match [.1, .2, .3, .2, .1]
    """
    def _random_harmony(self):
        return list([uniform(0, 1) for _ in range(5)])

    def _score(self, member):
        return 1./ sum(abs(member[i] - [.1, .2, .3, .2, .1][i]) for i in range(5))


def test_algorithm():
    algorithm = Algorithm(50, .5, .3, .01, 2000, max_score=None)
    algorithm.run()
