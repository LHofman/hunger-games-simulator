from Application.Port.IPrinter import IPrinter
from Domain.Tributes import Tributes

class GamePrinter:

  def __init__(self, printer: IPrinter) -> None:
    self.__printer = printer

  def printEnding(self, tributes: Tributes) -> None:
    tributesLeft = tributes.getTributes()

    if (len(tributesLeft) == 1): text = "%s has won!" % list(tributesLeft.values())[0].getName()
    else: text = 'Everyone has died, the game is over'

    self.__printer.print(text)

  def printFallenTributes(self, tributes: Tributes) -> None:
    recentDeaths = tributes.getRecentDeaths()

    if (len(recentDeaths) > 0):
      self.__printer.print("%d cannon shots can be heard in the distance." % len(recentDeaths))
      
      for playerName in recentDeaths:
        self.__printer.print("%s" % playerName)

      self.__printer.print("---")
    