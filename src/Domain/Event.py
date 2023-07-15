from Domain.Tribute import Tribute

class Event:
  
  def __init__(
    self,
    name: str,
    text: str,
    amountOfPlayers: int,
    deaths: list[str],
    allowedTimes: list[str]
  ) -> None:
    self.__name = name
    self.__text = text
    self.__amountOfPlayers = amountOfPlayers
    self.__deaths = deaths
    self.__allowedTimes = allowedTimes

  def getAmountOfPlayers(self) -> int:
    return self.__amountOfPlayers

  def getText(self) -> str:
    return self.__text

  def getDeaths(self) -> list[str]:
    return self.__deaths

  def getAllowedTimes(self) -> list[str]:
    return self.__allowedTimes
    