<div align="center">
    <img src="logo.png"></img>
</div>

<br>

[![Build Status](https://travis-ci.org/100/Solid.svg?branch=master)](https://travis-ci.org/100/Solid)
[![MIT License](https://img.shields.io/dub/l/vibe-d.svg)](https://github.com/100/Cranium/blob/master/LICENSE)

## *Solid* is a Python framework for gradient-free optimization.

#### It contains basic versions of many of the most common [optimization algorithms that do not require the calculation of gradients](https://en.wikipedia.org/wiki/Derivative-free_optimization), and allows for very rapid development using them.

#### It's a very versatile library that's great for learning, modifying, and of course, using out-of-the-box.

## See the detailed documentation [here](https://100.github.io/Solid/).

<hr>

## Current Features:
* [Genetic Algorithm](https://github.com/100/Solid/blob/master/Solid/GeneticAlgorithm.py)
* [Evolutionary Algorithm](https://github.com/100/Solid/blob/master/Solid/EvolutionaryAlgorithm.py)
* [Simulated Annealing](https://github.com/100/Solid/blob/master/Solid/SimulatedAnnealing.py)
* [Particle Swarm Optimization](https://github.com/100/Solid/blob/master/Solid/ParticleSwarm.py)
* [Tabu Search](https://github.com/100/Solid/blob/master/Solid/TabuSearch.py)
* [Harmony Search](https://github.com/100/Solid/blob/master/Solid/HarmonySearch.py)
* [Stochastic Hill Climb](https://github.com/100/Solid/blob/master/Solid/StochasticHillClimb.py)

<hr>

## Usage:
* ```pip install solidpy``` 
* Import the relevant algorithm
* Create a class that inherits from that algorithm, and that implements the necessary abstract methods
* Call its ```.run()``` method, which always returns the best solution and its objective function value

<hr>

## Example:

```python
from random import choice, randint, random
from string import lowercase
from Solid.EvolutionaryAlgorithm import EvolutionaryAlgorithm


class Algorithm(EvolutionaryAlgorithm):
    """
    Tries to get a randomly-generated string to match string "clout"
    """
    def _initial_population(self):
        return list(''.join([choice(lowercase) for _ in range(5)]) for _ in range(50))

    def _fitness(self, member):
        return float(sum(member[i] == "clout"[i] for i in range(5)))

    def _crossover(self, parent1, parent2):
        partition = randint(0, len(self.population[0]) - 1)
        return parent1[0:partition] + parent2[partition:]

    def _mutate(self, member):
        if self.mutation_rate >= random():
            member = list(member)
            member[randint(0,4)] = choice(lowercase)
            member = ''.join(member)
        return member


def test_algorithm():
    algorithm = Algorithm(.5, .7, 500, max_fitness=None)
    best_solution, best_objective_value = algorithm.run()

```

<hr>

## Testing

To run tests, look in the ```tests``` folder. 

Use [pytest](https://docs.pytest.org/en/latest/); it should automatically find the test files. 

<hr>

## Contributing

Feel free to send a pull request if you want to add any features or if you find a bug.

Check the issues tab for some potential things to do.

