import random

from Application.Port.IPrinter import IPrinter
from Domain.Event import Event
from Domain.Tribute import Tribute

class Tributes:

  def __init__(
    self,
    printer: IPrinter,
    tributes: list[Tribute]
  ) -> None:
    self.__printer = printer
    self.__tributes = tributes

  # Methods for Game round
  def nextRound(self) -> None:
    self.__tributesLeft = self.__tributes
    random.shuffle(self.__tributesLeft)
  
  def isRoundOver(self) -> bool:
    return len(self.__tributesLeft) == 0

  def getNextActiveTribute(self) -> Tribute:
    self.__activeTribute = self.__tributes.pop(0)
    self.__otherTributes = []

    return self.__activeTribute



  # Methods for Event
  def getOtherTributes(self, event: Event) -> list[Tribute]:
    amount = event.getAmountOfPlayers() - 1
    self.__otherTributes = self.__tributes[:amount]
    
    del self.__tributes[:amount]
    
    return self.__otherTributes

  def canPlayEvent(self, event: Event) -> bool:
    if (event.getAmountOfPlayers() > (len(self.__tributesLeft) + 1)): return False
    
    return True

  def printEvent(self, event: Event) -> None:
    text = event.getText()

    index = 0
    while (text.find("(Player") > -1):
      tribute = self.__getTributeFromEventText("Player%d" % (index + 1))
      text = text.replace("(Player%d)" % (index + 1), tribute.getName())
      index += 1

    self.__printer.print(text)
    
  def __getTributeFromEventText(self, player: str) -> Tribute:
    playerNumber = int(player[-1])
    
    if (playerNumber == 1): return self.__activeTribute
    else: return self.__otherTributes[playerNumber - 2]