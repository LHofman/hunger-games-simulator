from Application.Service.FileReader import FileReader
from Application.Service.Printer import Printer
from Domain.Tribute import Tribute
from Domain.Tributes import Tributes
from Domain.Repository.ITributeRepository import ITributeRepository

class TributeRepository(ITributeRepository):

  def __init__(self) -> None:
    self.__fileReader = FileReader()
    self.__printer = Printer()
  
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

    return Tributes(self.__printer, tributes)
    