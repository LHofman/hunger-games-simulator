"""Event rule that handles effects on the gamestate based on the time of the event."""

from Domain.EventRule import EventRule
from Domain.types import Event, GameRoundStateWithoutEvent


class TimedEvents(EventRule):
    """Event rule that handles effects on the gamestate based on the time of the event."""

    def canPlayEvent(
        self,
        event: Event,
        gameState: GameRoundStateWithoutEvent,
    ) -> bool:
        """Check if the event can be played based on the time of the event."""
        if 'time' not in event:
            return gameState['playStandardEvents']
        
        timesList = event['time']
        if not isinstance(timesList, list):
            timesList = [timesList]

        return gameState['time'] in timesList
