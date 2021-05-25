from pyker.game import *
from pyker.agents.humanDebug import *
from pyker.agents.naive import *

playerList = [
    HumanDebug(1000, "foo"),
    HumanDebug(1000, "bar"),
    Naive(1000, "random naive")
]
game = Game(playerList, 10)
winner = game.start()
print(winner.name)