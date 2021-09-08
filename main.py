from pyker.agents.AnnStartingHands import AnnBotStartingHands
from pyker.agents.ANNdecisionBot import AnnDecisionBot
from pyker.agents.ANNbot import AnnBot
from pyker.agents.humanDebug import HumanDebug
from pyker.agents.KNNbot import KnnBot
from pyker.agents.formulaBased import FormulaBasedAgent
from pyker.cards import Deck
from pyker.game import Poker

sbph = [0, 0, 0, 0]
passivity = [0, 0, 0, 0]
numOfGames = 0
for i in range(100):
    playerList = [
        FormulaBasedAgent('formula bot'),
        AnnBot('ann bot'),
        KnnBot('knn bot'),
        AnnBotStartingHands('ann bot + starting hands')
    ]
        
    game = Poker(playerList, Deck(), 32, 1000)
    winner = game.start()
    numOfGames += game.numOfGames
    for n in range(len(playerList)):
        sbph[n] += playerList[n].smallBets/playerList[n].handsPlayed if playerList[n].handsPlayed > 0 else 0
        passivity[n] += playerList[n].handsPlayed

for n in range(len(playerList)):
    print(playerList[n].name, ' -> ', sbph[n]/100, '\tpassive -> ', (100*passivity[n])/numOfGames)
