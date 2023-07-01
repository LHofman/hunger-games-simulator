from Application.Port.IRandomizer import IRandomizer
from Domain.Event import Event

class Events:

  def __init__(
    self,
    randomizer: IRandomizer,
    events: list[Event]
  ) -> None:
    self.__randomizer = randomizer
    self.__events = events

  def chooseEvent(self) -> Event:
    return self.__randomizer.chooseOne(self.__events)
    