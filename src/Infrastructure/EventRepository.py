from Application.Port.IFileReader import IFileReader
from Domain.Event import Event
from Domain.Events import Events
from Domain.TributeRequirement import TributeRequirement
from Domain.TributeUpdate import TributeUpdate
from Domain.Repository.IEventRepository import IEventRepository

class EventRepository(IEventRepository):

  def __init__(self, fileReader: IFileReader) -> None:
    self.__fileReader = fileReader
  
  def getAll(self) -> Events:
    eventsInput = self.__fileReader.read('events.json', 'json')

    events = []
    for (name, event) in eventsInput.items():
      if ("ignore" in event): continue

      allowedTimes = event.get("time", [])
      allowedTimes = allowedTimes if isinstance(allowedTimes, list) else [allowedTimes]
      
      tributeUpdates = event.get("tributeUpdates", [])
      tributeUpdates = list(map(
        lambda tributeUpdate: TributeUpdate(
          tributeUpdate["player"],
          tributeUpdate["type"],
          tributeUpdate["operation"],
          tributeUpdate["value"]
        ),
        tributeUpdates
      ))

      tributeRequirements = event.get("tributeRequirements", [])
      tributeRequirements = list(map(
        lambda tributeRequirement: TributeRequirement(
          tributeRequirement["player"],
          tributeRequirement["type"],
          tributeRequirement.get("operation", "has"),
          tributeRequirement["value"]
        ),
        tributeRequirements
      ))

      event = Event(
        name,
        event["text"],
        event.get("players", 1),
        event.get("deaths", []),
        allowedTimes,
        tributeUpdates,
        tributeRequirements
      )

      events.append(event)

    return events
