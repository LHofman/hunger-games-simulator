from Application.Service.Game import Game
from Infrastructure.TributeRepository import TributeRepository

tributeRepository = TributeRepository()

game = Game(tributeRepository)

game.init()
