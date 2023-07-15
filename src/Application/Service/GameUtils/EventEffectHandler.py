from Domain.Event import Event
from Domain.Tributes import Tributes

class EventEffectHandler:

  def handle(self, tributes: Tributes, event: Event) -> None:
    self.__handleDeaths(tributes, event.getDeaths())

  def __handleDeaths(self, tributes: Tributes, deaths: list[str]) -> None:
    for player in deaths:
      tribute = tributes.getTributeFromEventText(player)
      tributes.removeTribute(tribute)
