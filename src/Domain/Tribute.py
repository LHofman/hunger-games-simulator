class Tribute:
  
  def __init__(self, index: int, name: str) -> None:
    self.__index = index
    self.__name = name

  def getIndex(self) -> int:
    return self.__index

  def getName(self) -> str:
    return self.__name