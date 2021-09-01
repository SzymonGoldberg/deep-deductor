from pyker.agents.ANNbot import AnnBot
from pyker.agents.humanDebug import HumanDebug
from pyker.agents.KNNbot import KnnBot
from pyker.agents.formulaBased import FormulaBasedAgent
from pyker.cards import Deck
from pyker.game import Poker

stats = [0, 0]
passivity = [0, 0]
numOfGames = 0
for i in range(100):
    playerList = [
        FormulaBasedAgent('formula bot'),
        AnnBot('ann bot')
    ]
        
    game = Poker(playerList, Deck(), 32, 1000)
    winner = game.start()
    numOfGames += game.numOfGames
    for i in range(len(playerList)):
        stats[i] += playerList[i].smallBets/playerList[i].handsPlayed    
        passivity[i] += playerList[i].handsPlayed

print('formula -> ', stats[0]/10, '\tpassive -> ', (100*passivity[0])/numOfGames)
print('ann + start hand evaulation -> ', stats[1]/10, '\tpassive -> ', (100*passivity[1])/numOfGames)