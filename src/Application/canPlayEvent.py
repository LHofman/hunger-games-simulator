"""Check if an event can be played in the given game state."""

from Domain.eventRulesList import eventRulesList
from Domain.types import Event, GameRoundStateWithoutEvent


def canPlayEvent(gameState: GameRoundStateWithoutEvent):
    """Return a function that checks if an event can be played in the given game state."""

    def canPlayEventInner(event: Event) -> bool:
        for eventRule in eventRulesList:
            if not eventRule.canPlayEvent(event, gameState):
                return False
            
        return True

    return canPlayEventInner
