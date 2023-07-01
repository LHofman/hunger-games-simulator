from Domain.Event import Event

class Events:

  def __init__(self, events: list[Event]) -> None:
    self.__events = events
