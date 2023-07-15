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
    self.__playRound("The Bloodbath", "bloodbath", False)

    day = 0
    while (not self.__tributes.isGameOver()):
      day += 1
      self.__playRound("Day %d" % day, "day", True)
      self.__playRound("Night %d" % day, "night", True)
      if (day == 5): self.__playRound("The Feast", "feast", False)

    self.__tributes.printEnding()

  def __playRound(self, label: str, time: str, playStandardEvents: bool) -> None:
    if (self.__tributes.isGameOver()): return

    print(label)

    self.__tributes.nextRound()
    
    while (not self.__tributes.isRoundOver()):
      tribute = self.__tributes.getNextActiveTribute()
      self.__playTribute(tribute, time, playStandardEvents)
    
    print('--------------------------------')
    
  def __playTribute(self, tribute: Tribute, time: str, playStandardEvents: bool) -> None:
    event = self.__events.chooseEvent(tribute, self.__tributes, time, playStandardEvents)

    otherTributes = self.__tributes.getOtherTributes(event)

    self.__tributes.handleEventEffects(event)
    self.__tributes.printEvent(event)
    