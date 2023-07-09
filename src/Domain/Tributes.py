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

  def getNext(self, amount: int) -> list[Tribute]:
    next = self.__tributes[:amount]
    
    del self.__tributes[:amount]
    
    return next

  def canPlayEvent(self, tribute: Tribute, event: Event) -> bool:
    if (event.getAmountOfPlayers() > (len(self.__tributesLeft) + 1)): return False
    
    return True
