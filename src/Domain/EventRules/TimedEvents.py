from Domain.EventRule import EventRule
from Domain.types import Event, GameRoundStateWithoutEvent

class TimedEvents(EventRule):
    def canPlayEvent(
        self,
        event: Event,
        gameState: GameRoundStateWithoutEvent
    ) -> bool:
        if 'time' not in event:
            return gameState['playStandardEvents']
        
        timesList = event['time']
        if not isinstance(timesList, list):
            timesList = [timesList]

        return gameState['time'] in timesList
