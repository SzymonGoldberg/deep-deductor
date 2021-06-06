from pyker.agents.naive import Naive
from pyker.game import *
from pyker.agents.humanDebug import HumanDebug
from pyker.agents.formulaBased import FormulaBasedAgent
from pyker.agents.formulaBasedPotOdd import FormulaBasedPotOddAgent
from pyker.agents.naive import Naive

playerList = [
    HumanDebug(1000, "foo"),
    FormulaBasedAgent(1000, "formula based"),
    FormulaBasedPotOddAgent(1000, "pot odd"),
    Naive(1000, 'Naive')
]
game = Game(playerList, 10)
winner = game.start()
print(winner.name)