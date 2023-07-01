from Domain.Repository.ITributeRepository import ITributeRepository

class Game:

  def __init__(self, tributeRepository: ITributeRepository) -> None:
    self.__tributeRepository = tributeRepository

  def init(self) -> None:
    self.__tributes = self.__tributeRepository.getAll()
