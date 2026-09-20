"""Event rule that ignores events with the 'ignore' comment in their definition."""

from domain.event_rule import EventRule
from domain.types import Event, GameRoundStateWithoutEvent


class IgnoreComments(EventRule):
    """Event rule that ignores events with the 'ignore' comment in their definition."""

    def can_play_event(
        self,
        event: Event,
        game_state: GameRoundStateWithoutEvent,
    ) -> bool:
        """Check if the event can be played based on the 'ignore' comment."""
        return 'ignore' not in event
