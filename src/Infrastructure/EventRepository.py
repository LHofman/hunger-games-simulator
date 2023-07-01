from Application.Service.FileReader import FileReader
from Domain.Event import Event
from Domain.Events import Events
from Domain.Repository.IEventRepository import IEventRepository

class EventRepository(IEventRepository):

  def __init__(self) -> None:
    self.__fileReader = FileReader()
  
  def getAll(self) -> Events:
    eventsInput = self.__fileReader.read('events.json', 'json')

    # print(eventsInput.items())

    events = []
    for (name, event) in eventsInput.items():
      if ("ignore" in event): continue
      
      event = Event(
        name,
        event["text"]
      )

      events.append(event)

    return Events(events)