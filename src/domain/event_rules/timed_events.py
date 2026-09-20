"""Event rule that handles effects on the gamestate based on the time of the event."""

from domain.event_rule import EventRule
from domain.types import Event, GameRoundStateWithoutEvent


class TimedEvents(EventRule):
    """Event rule that handles effects on the gamestate based on the time of the event."""

    def can_play_event(
        self,
        event: Event,
        game_state: GameRoundStateWithoutEvent,
    ) -> bool:
        """Check if the event can be played based on the time of the event."""
        if 'time' not in event:
            return game_state['play_standard_events']
        
        times_list = event['time']
        if not isinstance(times_list, list):
            times_list = [times_list]

        return game_state['time'] in times_list
