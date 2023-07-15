from Application.Port.IPrinter import IPrinter
from Application.Port.IRandomizer import IRandomizer
from Application.Service.GameUtils.EventEffectHandler import EventEffectHandler
from Application.Service.GameUtils.EventPrinter import EventPrinter
from Application.Service.GameUtils.EventValidator import EventValidator
from Domain.Events import Events
from Domain.Tribute import Tribute
from Domain.Tributes import Tributes
from Domain.Repository.IEventRepository import IEventRepository
from Domain.Repository.ITributeRepository import ITributeRepository

class Game:

  def __init__(
    self,
    eventEffectHandler: EventEffectHandler,
    eventPrinter: EventPrinter,
    eventRepository: IEventRepository,
    eventValidator: EventValidator,
    printer: IPrinter,
    randomizer: IRandomizer,
    tributeRepository: ITributeRepository
  ) -> None:
    self.__eventEffectHandler = eventEffectHandler
    self.__eventPrinter = eventPrinter
    self.__eventRepository = eventRepository
    self.__eventValidator = eventValidator
    self.__printer = printer
    self.__randomizer = randomizer
    self.__tributeRepository = tributeRepository

  def init(self) -> None:
    self.__events = Events(
      self.__eventValidator,
      self.__randomizer,
      self.__eventRepository.getAll()
    )

    self.__tributes = Tributes(
      self.__printer,
      self.__tributeRepository.getAll()
    )

  def start(self) -> None:
    self.__playRound("The Bloodbath", "bloodbath", False)

    day = 0
    while (not self.__tributes.isGameOver()):
      day += 1
      self.__playRound("Day %d" % day, "day", True)
      self.__playRound("Night %d" % day, "night", True)
      if (day == 5): self.__playRound("The Feast", "feast", False)

    self.__printEnding()

  def __playRound(self, label: str, time: str, playStandardEvents: bool) -> None:
    if (self.__tributes.isGameOver()): return

    self.__printer.print(label)

    self.__tributes.nextRound()
    
    while (not self.__tributes.isRoundOver()):
      tribute = self.__tributes.getNextActiveTribute()
      self.__playTribute(tribute, time, playStandardEvents)
    
    self.__printer.print('--------------------------------')
    
  def __playTribute(self, tribute: Tribute, time: str, playStandardEvents: bool) -> None:
    event = self.__events.chooseEvent(self.__tributes, time, playStandardEvents)

    otherTributes = self.__tributes.getOtherTributes(event)

    self.__eventEffectHandler.handle(self.__tributes, event)
    self.__eventPrinter.print(self.__tributes, event)

  def __printEnding(self) -> None:
    tributesLeft = self.__tributes.getTributes()

    if (len(tributesLeft) == 1): text = "%s has won!" % list(tributesLeft.values())[0].getName()
    else: text = 'Everyone has died, the game is over'

    self.__printer.print(text)
