from Domain.Tribute import Tribute

class Event:
  
  def __init__(
    self,
    name: str,
    text: str,
    amountOfPlayers: int
  ) -> None:
    self.__name = name
    self.__text = text
    self.__amountOfPlayers = amountOfPlayers

  def getAmountOfPlayers(self) -> int:
    return self.__amountOfPlayers

  def getText(self) -> str:
    return self.__text
