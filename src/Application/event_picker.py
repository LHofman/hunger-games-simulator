"""Event picker for the Hunger Games simulator."""

import random

from application.can_play_event import can_play_event
from domain.types import GameRoundStateWithoutEvent, Event, IncreaseEventOdds


class EventPicker:
    """Pick an event based on the current game state."""

    def get_event(self, game_state: GameRoundStateWithoutEvent) -> Event:
        """Return a random event based on the current game state."""
        event_options = list(game_state['events'].values())

        # (In/De)crease event odds.
        increase_odds_events = self._get_increased_odds_events(game_state)
        event_options = self._update_events_options_based_on_odds(
            game_state,
            increase_odds_events,
        )

        # Remove events unable to occur at this moment.
        event_options = list(filter(can_play_event(game_state), event_options))

        if len(event_options) == 0:
            print('hi')
            print(increase_odds_events)
            print(game_state)

        # Get random event.
        event = random.choice(event_options)

        if event['name'] in game_state['events_occured']:
            game_state['events_occured'][event['name']] += 1
        else:
            game_state['events_occured'][event['name']] = 1

        return event

    def _get_increased_odds_events(
        self,
        game_state: GameRoundStateWithoutEvent,
    ) -> list[IncreaseEventOdds]:
        return (
            self._get_increased_odds_events_from_possessions(game_state)
            + self._get_increased_odds_events_from_game_speed(game_state)
            + self._get_default_increased_odds_events(game_state)
        )

    def _get_increased_odds_events_from_possessions(
        self,
        game_state: GameRoundStateWithoutEvent,
    ) -> list[IncreaseEventOdds]:
        tribute = game_state['current_tribute']
        increased_odds_events_options = (
            game_state['increase_event_odds']['possessions']
        )

        increased_odds_events: list[IncreaseEventOdds] = []
        for (type, values) in tribute['possessions'].items():
            if type not in increased_odds_events_options: continue

            for value in values:
                if value in increased_odds_events_options[type]:
                    increased_odds_events.extend(
                        increased_odds_events_options[type][value],
                    )

        return increased_odds_events

    def _get_increased_odds_events_from_game_speed(
        self,
        game_state: GameRoundStateWithoutEvent,
    ) -> list[IncreaseEventOdds]:
        game_speed = game_state['options']['speed']
        events = game_state['events']

        increased_odds_events: list[IncreaseEventOdds] = []

        if game_speed < 1 or game_speed > 10 or game_speed == 5:
            return []

        diff = abs(game_speed - 5)
        multiplier = diff / 5
        percentage = (1 if game_speed > 5 else -1) * 100 * multiplier
        for (name, event) in list(events.items()):
            if 'deaths' in event:
                increased_odds_events.append(
                    {'event': name, 'percentage': percentage},
                )

        return increased_odds_events

    def _get_default_increased_odds_events(
        self,
        game_state: GameRoundStateWithoutEvent,
    ) -> list[IncreaseEventOdds]:
        events = game_state['events']
        events_occured = game_state['events_occured']

        increased_odds_events: list[IncreaseEventOdds] = []

        for (name, event) in events.items():
            if (
                'max_occurances' in event
                 and name in events_occured
                 and event['max_occurances'] == events_occured[name]
            ): increased_odds_events.append(
                { 'event': name, 'percentage': -100 },
            )
            elif 'percentage' in event:
                increased_odds_events.append(
                    { 'event': name, 'percentage': event['percentage'] },
                )

        return increased_odds_events

    def _update_events_options_based_on_odds(
        self,
        game_state: GameRoundStateWithoutEvent,
        increased_odds_events: list[IncreaseEventOdds],
    ) -> list[Event]:
        events = game_state['events']
        event_options = list(game_state['events'].values())

        for increase_event in increased_odds_events:
            percentage = increase_event['percentage']
            if percentage > 0:
                while (percentage >= 100):
                    event_options.append(events[increase_event['event']])
                    percentage -= 100
                rnd = random.random() * 100
                if rnd < percentage:
                    event_options.append(events[increase_event['event']])
            else:
                rnd = random.random() * 100
                if (
                    rnd < abs(percentage)
                    and events[increase_event['event']] in event_options
                ): event_options.remove(events[increase_event['event']])
        
        return event_options
