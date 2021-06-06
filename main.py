from pyker.agents.naive import Naive
from pyker.game import *
from pyker.agents.humanDebug import HumanDebug
from pyker.agents.formulaBased import FormulaBasedAgent
from pyker.agents.naive import Naive

playerList = [
    HumanDebug(1000, "foo"),
    HumanDebug(1000, "bar"),
    FormulaBasedAgent(1000, "formula based")
]
game = Game(playerList, 10)
winner = game.start()
print(winner.name)