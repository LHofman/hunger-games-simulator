from Application.Port.IPrinter import IPrinter
from Domain.Tribute import Tribute
from Domain.Tributes import Tributes

class Event:
  
  def __init__(
    self,
    printer: IPrinter,
    name: str,
    text: str,
    amountOfPlayers: int
  ) -> None:
    self.__printer = printer
    self.__name = name
    self.__text = text
    self.__amountOfPlayers = amountOfPlayers

  def getAmountOfPlayers(self) -> int:
    return self.__amountOfPlayers

  def canPlayEvent(self, tribute: Tribute, tributes: Tributes) -> bool:
    if (self.__amountOfPlayers > (len(tributes.getTributesLeft()) + 1)): return False
    
    return True

  def print(self, tributes: list[Tribute]) -> None:
    text = self.__text

    index = 0
    while (text.find("(Player") > -1):
      tribute = tributes[index]
      text = text.replace("(Player%d)" % (index + 1), tributes[index].getName())
      index += 1

    self.__printer.print(text)
    