from pyker.game import *
from pyker.agents.humanDebug import HumanDebug
from pyker.cards import Deck

playerList = [
    HumanDebug(1000, 'foo'), 
    HumanDebug(1000, 'bar'), 
    HumanDebug(1000, 'nice')]
    
game = Game(playerList, Deck(), 32)
winner = game.start()
print(winner.agent.name)