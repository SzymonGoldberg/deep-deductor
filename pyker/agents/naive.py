from pyker.roundData import Move
from pyker.agents.base import Agent
import random

class Naive(Agent):
    def bet(self, moves, roundData):
        if len(moves) > 1:
            moves.pop(moves.index(Move.QUIT))
        return random.choice(moves)