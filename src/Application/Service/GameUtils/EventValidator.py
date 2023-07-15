from Domain.Event import Event
from Domain.Tributes import Tributes

class EventValidator:

  def canPlayEvent(self, tributes: Tributes, event: Event, time: str, playStandardEvents: bool) -> bool:
    if (event.getAmountOfPlayers() > (len(tributes.getTributesLeft()) + 1)): return False
    if (not self.__canPlayTimedEvent(event, time, playStandardEvents)): return False
    
    return True

  def __canPlayTimedEvent(self, event: Event, time: str, playStandardEvents: bool) -> bool:
    allowedTimes = event.getAllowedTimes()

    if (len(allowedTimes) == 0):
      return playStandardEvents
    else:
      return time in allowedTimes
