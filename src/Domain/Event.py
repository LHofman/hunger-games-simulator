from Domain.Tribute import Tribute
from Domain.TributeRequirement import TributeRequirement
from Domain.TributeUpdate import TributeUpdate

class Event:
  
  def __init__(
    self,
    name: str,
    text: str,
    amountOfPlayers: int,
    deaths: list[str],
    allowedTimes: list[str],
    tributeUpdates: list[TributeUpdate],
    tributeRequirements: list[TributeRequirement]
  ) -> None:
    self.__name = name
    self.__text = text
    self.__amountOfPlayers = amountOfPlayers
    self.__deaths = deaths
    self.__allowedTimes = allowedTimes
    self.__tributeUpdates = tributeUpdates
    self.__tributeRequirements = tributeRequirements

  def getAmountOfPlayers(self) -> int:
    return self.__amountOfPlayers

  def getText(self) -> str:
    return self.__text

  def getDeaths(self) -> list[str]:
    return self.__deaths

  def getAllowedTimes(self) -> list[str]:
    return self.__allowedTimes
    
  def getTributeUpdates(self) -> list[TributeUpdate]:
    return self.__tributeUpdates
    
  def getTributeRequirements(self) -> list[TributeRequirement]:
    return self.__tributeRequirements
    