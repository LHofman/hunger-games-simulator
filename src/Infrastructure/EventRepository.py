from Application.Service.FileReader import FileReader
from Application.Service.Printer import Printer
from Application.Service.Randomizer import Randomizer
from Domain.Event import Event
from Domain.Events import Events
from Domain.Repository.IEventRepository import IEventRepository

class EventRepository(IEventRepository):

  def __init__(self) -> None:
    self.__fileReader = FileReader()
    self.__printer = Printer()
    self.__randomizer = Randomizer()
  
  def getAll(self) -> Events:
    eventsInput = self.__fileReader.read('events.json', 'json')

    events = []
    for (name, event) in eventsInput.items():
      if ("ignore" in event): continue
      
      event = Event(
        self.__printer,
        name,
        event["text"],
        event.get("players", 1)
      )

      events.append(event)

    return Events(self.__randomizer, events)