class TributeRequirement:
  
  def __init__(self, player: int, type: str, operation: str, value) -> None:
    self.__player = player
    self.__type = type
    self.__operation = operation
    self.__value = value

  def getPlayer(self) -> int:
    return self.__player

  def getType(self) -> str:
    return self.__type

  def checkList(self, tributeData) -> bool:
    match (self.__operation):
      case 'has':
        if self.__value == 'any': return len(tributeData) > 0
        else: return self.__value in tributeData
      case 'not':
        if self.__value == 'any': return len(tributeData) == 0
        else: return not self.__value in tributeData
      case _:
        return True
