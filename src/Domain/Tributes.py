import random

from Domain.Events import Events
from Domain.Tribute import Tribute

class Tributes:

  def __init__(self, tributes: list[Tribute]) -> None:
    self.__tributes = tributes

  def playRound(self, events: Events) -> None:
    random.shuffle(self.__tributes)

    for tribute in self.__tributes:
      tribute.playRound(events)
