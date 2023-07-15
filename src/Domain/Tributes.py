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

  def isGameOver(self) -> bool:
    return len(self.__tributes) <= 1
  
  def isRoundOver(self) -> bool:
    return len(self.__tributesLeft) == 0 or self.isGameOver()

  def getNextActiveTribute(self) -> Tribute:
    self.__activeTribute = self.__tributesLeft.pop(0)
    self.__otherTributes = []

    return self.__activeTribute

  def printEnding(self) -> None:
    if (len(self.__tributes) == 1): text = "%s has won!" % list(self.__tributes.values())[0].getName()
    else: text = 'Everyone has died, the game is over'

    self.__printer.print(text)



  # Methods for Event
  def getOtherTributes(self, event: Event) -> list[Tribute]:
    amount = event.getAmountOfPlayers() - 1
    self.__otherTributes = self.__tributesLeft[:amount]
    
    del self.__tributesLeft[:amount]
    
    return self.__otherTributes

  def canPlayEvent(self, event: Event, time: str, playStandardEvents: bool) -> bool:
    if (event.getAmountOfPlayers() > (len(self.__tributesLeft) + 1)): return False
    if (not self.__canPlayTimedEvent(event, time, playStandardEvents)): return False
    
    return True

  def __canPlayTimedEvent(self, event: Event, time: str, playStandardEvents: bool) -> bool:
    allowedTimes = event.getAllowedTimes()

    if (len(allowedTimes) == 0):
      return playStandardEvents
    else:
      return time in allowedTimes

  def handleEventEffects(self, event: Event) -> None:
    self.__handleDeaths(event.getDeaths())

  def __handleDeaths(self, deaths: list[str]) -> None:
    for player in deaths:
      tribute = self.__getTributeFromEventText(player)
      del self.__tributes[tribute.getIndex()]

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
    