from Domain.TributeRequirement import TributeRequirement
from Domain.TributeUpdate import TributeUpdate

class Tribute:
  
  def __init__(self, index: int, name: str) -> None:
    self.__index = index
    self.__name = name
    self.__items = []
    self.__statuses = set()
    self.__kills = 0

  def getIndex(self) -> int:
    return self.__index

  def getName(self) -> str:
    return self.__name

  def checkDataRequirement(self, tributeRequirement: TributeRequirement) -> bool:
    match (tributeRequirement.getType()):
      case 'item':
        return tributeRequirement.checkList(self.__items)
      case 'status':
        return tributeRequirement.checkList(self.__statuses)
      case _:
        return True

  def updateData(self, tributeUpdate: TributeUpdate) -> None:
    match (tributeUpdate.getType()):
      case 'item':
        tributeUpdate.updateList(self.__items)
      case 'status':
        tributeUpdate.updateSet(self.__statuses)
      case 'kills':
        self.__kills = tributeUpdate.updateInteger(self.__kills)
