from pyker.game import *
from pyker.agents.humanDebug import *

playerList = [
    HumanDebug(1000, "foo"),
    HumanDebug(1000, "bar")
]
game = Game(playerList, 10)
winner = game.start()
print(winner.name)