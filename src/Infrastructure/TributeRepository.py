from Application.Port.IFileReader import IFileReader
from Domain.Tribute import Tribute
from Domain.Tributes import Tributes
from Domain.Repository.ITributeRepository import ITributeRepository

class TributeRepository(ITributeRepository):

  def __init__(self, fileReader: IFileReader) -> None:
    self.__fileReader = fileReader
  
  def getAll(self) -> Tributes:
    names = self.__fileReader.read('tributes.txt')

    tributes = dict()
    index = 0
    for name in names:      
      index += 1
      tribute = Tribute(
        index,
        name
      )

      tributes[index] = tribute

    return tributes
    