import random

class Bot_Base_Class:
    def __init__(self, seed=None):
        """
        seed: optional integer for deterministic behavior.
              If None, tie-breaking is random each run.
        """
        self.seed = seed
        self.reset_rng()

    def reset_rng(self):
        """
        Reset the internal RNG for deterministic behavior.
        """
        self.rng = random.Random(self.seed) if self.seed is not None else random

    def choose_move(self, state):
        """
        Given an IsolationState, return a legal move (r, c)
        """
        raise NotImplementedError