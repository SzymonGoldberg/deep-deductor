from pyker.agents.KNNbot import KnnBot
from pyker.agents.formulaBased import FormulaBasedAgent
from pyker.agents.humanDebug import HumanDebug
from pyker.cards import Deck
from pyker.game import *

playerList = [
    HumanDebug(1000, 'foo'), 
    KnnBot(1000, 'knn bot')
]
    
game = Game(playerList, Deck(), 32)
winner = game.start()
print(winner.agent.name)