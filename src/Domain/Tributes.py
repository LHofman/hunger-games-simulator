import random

from Domain.Event import Event
from Domain.Tribute import Tribute

class Tributes:

  def __init__(self, tributes: list[Tribute]) -> None:
    self.__tributes = tributes

  def nextRound(self) -> None:
    self.__tributesLeft = self.__tributes
    random.shuffle(self.__tributesLeft)
  
  def isRoundOver(self) -> bool:
    return len(self.__tributesLeft) == 0

  def getNextActiveTribute(self) -> Tribute:
    self.__activeTribute = self.__tributes.pop(0)
    self.__otherTributes = []

    return self.__activeTribute

  def getOtherTributes(self, event: Event) -> list[Tribute]:
    amount = event.getAmountOfPlayers()
    self.__otherTributes = self.__tributes[:amount]
    
    del self.__tributes[:amount]
    
    return self.__otherTributes

  def canPlayEvent(self, event: Event) -> bool:
    if (event.getAmountOfPlayers() > (len(self.__tributesLeft) + 1)): return False
    
    return True
