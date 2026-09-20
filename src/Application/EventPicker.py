"""Event picker for the Hunger Games simulator."""

import random

from Application.canPlayEvent import canPlayEvent
from Domain.types import GameRoundStateWithoutEvent, Event, IncreaseEventOdds


class EventPicker:
    """Pick an event based on the current game state."""

    def getEvent(self, gameState: GameRoundStateWithoutEvent) -> Event:
        """Return a random event based on the current game state."""
        eventOptions = list(gameState['events'].values())

        # (In/De)crease event odds.
        increaseOddsEvents = self._getIncreasedOddsEvents(gameState)
        eventOptions = self._updateEventsOptionsBasedOnOdds(
            gameState,
            increaseOddsEvents,
        )

        # Remove events unable to occur at this moment.
        eventOptions = list(filter(canPlayEvent(gameState), eventOptions))

        if len(eventOptions) == 0:
            print('hi')
            print(increaseOddsEvents)
            print(gameState)

        # Get random event.
        event = random.choice(eventOptions)

        if event['name'] in gameState['eventsOccured']:
            gameState['eventsOccured'][event['name']] += 1
        else:
            gameState['eventsOccured'][event['name']] = 1

        return event

    def _getIncreasedOddsEvents(
        self,
        gameState: GameRoundStateWithoutEvent,
    ) -> list[IncreaseEventOdds]:
        return (
            self._getIncreasedOddsEventsFromPossessions(gameState)
            + self._getIncreasedOddsEventsFromGameSpeed(gameState)
            + self._getDefaultIncreasedOddsEvents(gameState)
        )

    def _getIncreasedOddsEventsFromPossessions(
        self,
        gameState: GameRoundStateWithoutEvent,
    ) -> list[IncreaseEventOdds]:
        tribute = gameState['currentTribute']
        increasedOddsEventsOptions = (
            gameState['increaseEventOdds']['possessions']
        )

        increasedOddsEvents: list[IncreaseEventOdds] = []
        for (type, values) in tribute['possessions'].items():
            if type not in increasedOddsEventsOptions: continue

            for value in values:
                if value in increasedOddsEventsOptions[type]:
                    increasedOddsEvents.extend(
                        increasedOddsEventsOptions[type][value],
                    )

        return increasedOddsEvents

    def _getIncreasedOddsEventsFromGameSpeed(
        self,
        gameState: GameRoundStateWithoutEvent,
    ) -> list[IncreaseEventOdds]:
        gameSpeed = gameState['options']['speed']
        events = gameState['events']

        increasedOddsEvents: list[IncreaseEventOdds] = []

        if gameSpeed < 1 or gameSpeed > 10 or gameSpeed == 5:
            return []

        diff = abs(gameSpeed - 5)
        multiplier = diff / 5
        percentage = (1 if gameSpeed > 5 else -1) * 100 * multiplier
        for (name, event) in list(events.items()):
            if 'deaths' in event:
                increasedOddsEvents.append(
                    {'event': name, 'percentage': percentage},
                )

        return increasedOddsEvents

    def _getDefaultIncreasedOddsEvents(
        self,
        gameState: GameRoundStateWithoutEvent,
    ) -> list[IncreaseEventOdds]:
        events = gameState['events']
        eventsOccured = gameState['eventsOccured']

        increasedOddsEvents: list[IncreaseEventOdds] = []

        for (name, event) in events.items():
            if (
                'maxOccurances' in event
                 and name in eventsOccured
                 and event['maxOccurances'] == eventsOccured[name]
            ): increasedOddsEvents.append(
                { 'event': name, 'percentage': -100 },
            )
            elif 'percentage' in event:
                increasedOddsEvents.append(
                    { 'event': name, 'percentage': event['percentage'] },
                )

        return increasedOddsEvents

    def _updateEventsOptionsBasedOnOdds(
        self,
        gameState: GameRoundStateWithoutEvent,
        increasedOddsEvents: list[IncreaseEventOdds],
    ) -> list[Event]:
        events = gameState['events']
        eventOptions = list(gameState['events'].values())

        for increaseEvent in increasedOddsEvents:
            percentage = increaseEvent['percentage']
            if percentage > 0:
                while (percentage >= 100):
                    eventOptions.append(events[increaseEvent['event']])
                    percentage -= 100
                rnd = random.random() * 100
                if rnd < percentage:
                    eventOptions.append(events[increaseEvent['event']])
            else:
                rnd = random.random() * 100
                if (
                    rnd < abs(percentage)
                    and events[increaseEvent['event']] in eventOptions
                ): eventOptions.remove(events[increaseEvent['event']])
        
        return eventOptions
