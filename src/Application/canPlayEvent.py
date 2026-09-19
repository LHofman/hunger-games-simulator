from Domain.eventRulesList import eventRulesList
from Domain.types import Event, GameRoundStateWithoutEvent

def canPlayEvent(gameState: GameRoundStateWithoutEvent):
  def canPlayEventInner(event: Event) -> bool:
    for eventRule in eventRulesList:
      if not eventRule.canPlayEvent(event, gameState):
        return False
      
    return True

  return canPlayEventInner
