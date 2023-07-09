from Domain.Tribute import Tribute
from Domain.Repository.IEventRepository import IEventRepository
from Domain.Repository.ITributeRepository import ITributeRepository

class Game:

  def __init__(
    self,
    eventRepository: IEventRepository,
    tributeRepository: ITributeRepository
  ) -> None:
    self.__eventRepository = eventRepository
    self.__tributeRepository = tributeRepository

  def init(self) -> None:
    self.__events = self.__eventRepository.getAll()
    self.__tributes = self.__tributeRepository.getAll()

  def start(self) -> None:
    while (not self.__tributes.isGameOver()):
      self.__playRound()
      print('--------------------------------')
    
    self.__tributes.printEnding()

  def __playRound(self) -> None:
    self.__tributes.nextRound()
    
    while (not self.__tributes.isRoundOver()):
      tribute = self.__tributes.getNextActiveTribute()
      self.__playTribute(tribute)
    
  def __playTribute(self, tribute: Tribute) -> None:
    event = self.__events.chooseEvent(tribute, self.__tributes)

    otherTributes = self.__tributes.getOtherTributes(event)

    self.__tributes.handleEventEffects(event)
    self.__tributes.printEvent(event)