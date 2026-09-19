from Domain.EventRule import EventRule
from Domain.types import Event, GameRoundStateWithoutEvent

class IgnoreComments(EventRule):
  def canPlayEvent(
    self,
    event: Event,
    gameState: GameRoundStateWithoutEvent
  ) -> bool:
    return 'ignore' not in event
