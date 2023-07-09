from Application.Service.FileReader import FileReader
from Application.Service.Randomizer import Randomizer
from Domain.Event import Event
from Domain.Events import Events
from Domain.Repository.IEventRepository import IEventRepository

class EventRepository(IEventRepository):

  def __init__(self) -> None:
    self.__fileReader = FileReader()
    self.__randomizer = Randomizer()
  
  def getAll(self) -> Events:
    eventsInput = self.__fileReader.read('events.json', 'json')

    events = []
    for (name, event) in eventsInput.items():
      if ("ignore" in event): continue
      
      event = Event(
        name,
        event["text"],
        event.get("players", 1),
        event.get("deaths", [])
      )

      events.append(event)

    return Events(self.__randomizer, events)