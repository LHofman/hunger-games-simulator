from Application.Service.Game import Game
from Infrastructure.EventRepository import EventRepository
from Infrastructure.TributeRepository import TributeRepository

eventRepository = EventRepository()
tributeRepository = TributeRepository()

game = Game(
  eventRepository,
  tributeRepository
)

game.init()
game.start()
