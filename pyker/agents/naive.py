from pyker.agents.base import Agent
import random

class Naive(Agent):
    def bet(self, moves, roundData):
        return random.choice(moves)