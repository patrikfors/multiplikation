"""Provides a Random wrapper that has a seed access method."""

from random import Random

class RandomWithSeed(Random):
    """Stupid class just to be able to get the seed value, which doesnt work anyway"""
    def __init__(self, x):
        Random.__init__(self, x)

    def seed(self, a=None, version=2):
        self.the_seed = a
        super(RandomWithSeed, self).seed(a, version)

    def get_seed(self):
        """Return the seed used when initializing."""
        return self.the_seed

if __name__ == '__main__':
    TEST_PRNG = RandomWithSeed(100)
    assert TEST_PRNG.get_seed() == 100

    print("Yup, seed is 100.")
