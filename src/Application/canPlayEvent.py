from Domain.eventRulesList import eventRulesList
from Domain.types import Event, GameRoundStateWithoutEvent

def canPlayEvent(gameState: GameRoundStateWithoutEvent):
  def canPlayEvent(event: Event) -> bool:
    for eventRule in eventRulesList:
      if not eventRule.canPlayEvent(event, gameState):
        return False
      
    return True

  return canPlayEvent
