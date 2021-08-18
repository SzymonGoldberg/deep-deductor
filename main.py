from pyker.agents.humanDebug import HumanDebug
from pyker.agents.KNNbot import KnnBot
from pyker.agents.formulaBased import FormulaBasedAgent
from pyker.cards import Deck
from pyker.game import *

playerList = [
    FormulaBasedAgent(1000, 'formula bot'),
    KnnBot(1000, 'knn bot')
]
    
game = Game(playerList, Deck(), 32)
winner = game.start()
for player in playerList:
    print(player.name, player.smallBets/player.handsPlayed if player.handsPlayed else 0)