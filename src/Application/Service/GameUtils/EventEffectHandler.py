from Domain.Event import Event
from Domain.Tributes import Tributes
from Domain.TributeUpdate import TributeUpdate

class EventEffectHandler:

  def handle(self, tributes: Tributes, event: Event) -> None:
    self.__handleDeaths(tributes, event.getDeaths())
    self.__handleTributeUpdates(tributes, event.getTributeUpdates())

  def __handleDeaths(self, tributes: Tributes, deaths: list[str]) -> None:
    for player in deaths:
      tribute = tributes.getTributeFromEventText(player)
      tributes.removeTribute(tribute)

  def __handleTributeUpdates(self, tributes: Tributes, tributeUpdates: list[TributeUpdate]) -> None:
    for tributeUpdate in tributeUpdates:
      tribute = tributes.getTributeFromEventText("player%d" % tributeUpdate.getPlayer())
      tribute.updateData(tributeUpdate)
