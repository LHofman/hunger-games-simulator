import random

from Application.Port.IPrinter import IPrinter
from Domain.Event import Event
from Domain.Tribute import Tribute

class Tributes:

  def __init__(
    self,
    printer: IPrinter,
    tributes: dict[int, Tribute]
  ) -> None:
    self.__printer = printer
    self.__tributes = tributes

  # Methods for Game round
  def nextRound(self) -> None:
    self.__tributesLeft = list(self.__tributes.values())
    random.shuffle(self.__tributesLeft)

  def getTributesLeft(self) -> list[Tribute]:
    return self.__tributesLeft

  def isGameOver(self) -> bool:
    return len(self.__tributes) <= 1
  
  def isRoundOver(self) -> bool:
    return len(self.__tributesLeft) == 0 or self.isGameOver()

  def getNextActiveTribute(self) -> Tribute:
    self.__activeTribute = self.__tributesLeft.pop(0)
    self.__otherTributes = []

    return self.__activeTribute

  def getTributes(self) -> dict[int, Tribute]:
    return self.__tributes

  # Methods for Event
  def getOtherTributes(self, event: Event) -> list[Tribute]:
    amount = event.getAmountOfPlayers() - 1
    self.__otherTributes = self.__tributesLeft[:amount]
    
    del self.__tributesLeft[:amount]
    
    return self.__otherTributes

  def removeTribute(self, tribute: Tribute) -> None:
    del self.__tributes[tribute.getIndex()]

  def getTributeFromEventText(self, player: str) -> Tribute:
    playerNumber = int(player[-1])
    
    if (playerNumber == 1): return self.__activeTribute
    else: return self.__otherTributes[playerNumber - 2]
