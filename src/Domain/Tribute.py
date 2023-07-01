from Domain.Events import Events

class Tribute:
  
  def __init__(self, index: int, name: str) -> None:
    self.__index = index
    self.__name = name

  def playRound(self, events: Events) -> None:
    event = events.chooseEvent()

    event.print(self.__name)
    