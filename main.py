from pyker.agents.humanDebug import HumanDebug
from pyker.agents.KNNbot import KnnBot
from pyker.agents.formulaBased import FormulaBasedAgent
from pyker.cards import Deck
from pyker.game import Poker

playerList = [
    HumanDebug('foo'),
    FormulaBasedAgent('formula bot'),
    KnnBot('knn bot')
]
    
game = Poker(playerList, Deck(), 32, 1000)
winner = game.start()
for player in playerList:
    print(player.name, player.smallBets/player.handsPlayed if player.handsPlayed else 0)