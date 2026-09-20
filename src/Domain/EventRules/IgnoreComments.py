"""Event rule that ignores events with the 'ignore' comment in their definition."""

from Domain.EventRule import EventRule
from Domain.types import Event, GameRoundStateWithoutEvent


class IgnoreComments(EventRule):
    """Event rule that ignores events with the 'ignore' comment in their definition."""

    def canPlayEvent(
        self,
        event: Event,
        gameState: GameRoundStateWithoutEvent,
    ) -> bool:
        """Check if the event can be played based on the 'ignore' comment."""
        return 'ignore' not in event
