from Application.Service.Game import Game
from Application.Service.GameUtils.EventEffectHandler import EventEffectHandler
from Application.Service.GameUtils.EventPrinter import EventPrinter
from Application.Service.GameUtils.EventValidator import EventValidator
from Application.Service.Utils.FileReader import FileReader
from Application.Service.Utils.Printer import Printer
from Application.Service.Utils.Randomizer import Randomizer
from Infrastructure.EventRepository import EventRepository
from Infrastructure.TributeRepository import TributeRepository


fileReader = FileReader()
printer = Printer()
randomizer = Randomizer()

eventEffectHandler = EventEffectHandler()
eventPrinter = EventPrinter(printer)
eventValidator = EventValidator()

eventRepository = EventRepository(fileReader)
tributeRepository = TributeRepository(fileReader)

game = Game(
  eventEffectHandler,
  eventPrinter,
  eventRepository,
  eventValidator,
  printer,
  randomizer,
  tributeRepository
)

game.init()
game.start()
