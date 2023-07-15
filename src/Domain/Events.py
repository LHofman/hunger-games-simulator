from Application.Port.IRandomizer import IRandomizer
from Application.Service.GameUtils.EventValidator import EventValidator
from Domain.Event import Event
from Domain.Tributes import Tributes

class Events:

  def __init__(
    self,
    eventValidator: EventValidator,
    randomizer: IRandomizer,
    events: list[Event]
  ) -> None:
    self.__eventValidator = eventValidator
    self.__randomizer = randomizer
    self.__events = events

  def chooseEvent(self, tributes: Tributes, time: str, playStandardEvents: bool) -> Event:
    eventsFiltered = list(filter(
      lambda event : self.__eventValidator.canPlayEvent(tributes, event, time, playStandardEvents),
      self.__events
    ))

    return self.__randomizer.chooseOne(eventsFiltered)
    