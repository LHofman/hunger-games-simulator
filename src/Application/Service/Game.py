from Domain.Repository.IEventRepository import IEventRepository
from Domain.Repository.ITributeRepository import ITributeRepository

class Game:

  def __init__(
    self,
    eventRepository: IEventRepository,
    tributeRepository: ITributeRepository
  ) -> None:
    self.__eventRepository = eventRepository
    self.__tributeRepository = tributeRepository

  def init(self) -> None:
    self.__events = self.__eventRepository.getAll()
    self.__tributes = self.__tributeRepository.getAll()
