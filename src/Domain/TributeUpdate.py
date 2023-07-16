class TributeUpdate:
  
  def __init__(self, player: int, type: str, operation: str, value) -> None:
    self.__player = player
    self.__type = type
    self.__operation = operation
    self.__value = value

  def getPlayer(self) -> int:
    return self.__player

  def getType(self) -> str:
    return self.__type

  def updateList(self, tributeData) -> None:
    match (self.__operation):
      case 'add':
        tributeData.append(self.__value)
      case 'remove':
        tributeData.remove(self.__value)

  def updateSet(self, tributeData) -> None:
    match (self.__operation):
      case 'add':
        tributeData.add(self.__value)
      case 'remove':
        tributeData.discard(self.__value)

  def updateInteger(self, tributeData) -> int:
    match (self.__operation):
      case 'add':
        return tributeData + self.__value
      case 'remove':
        return tributeData - self.__value
      case _:
        return tributeData
