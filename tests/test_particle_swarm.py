from Solid.ParticleSwarm import ParticleSwarm


class Algorithm(ParticleSwarm):
    """
    Tries to get a randomly-generated list to match [.1, .2, .3, .2, .1]
    """
    def _objective(self, member):
        return sum(abs(member[i] - [.1, .2, .3, .2, .1][i]) if (member[i] > 0 or member[i] < 0) else 1 for i in range(5))


def test_algorithm():
    algorithm = Algorithm(50, 5, [0.,0.,0.,0.,0.], [1.,1.,1.,1.,1.], 1., 2., 2., 500, min_objective=None)
    algorithm.run()
