from pyker import *
from pyker.agents.humanDebug import *

playerList = [
    HumanDebug(1000, "foo"),
    HumanDebug(1000, "bar")
]
game = Game(playerList, 10)
game.StartRound()