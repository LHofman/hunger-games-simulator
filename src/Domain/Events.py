from Application.Port.IRandomizer import IRandomizer
from Domain.Event import Event
from Domain.Tribute import Tribute
from Domain.Tributes import Tributes

class Events:

  def __init__(
    self,
    randomizer: IRandomizer,
    events: list[Event]
  ) -> None:
    self.__randomizer = randomizer
    self.__events = events

  def chooseEvent(self, tribute: Tribute, tributes: Tributes) -> Event:
    eventsFiltered = list(filter(
      lambda event: tributes.canPlayEvent(tribute, event),
      self.__events
    ))

    return self.__randomizer.chooseOne(eventsFiltered)
    