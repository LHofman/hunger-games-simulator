from typing import TypedDict

import pytest

from domain.event_rules.timed_events import TimedEvents
from domain.types import Event
from tests.defaults import (
    default_event,
    default_game_round_state_without_event,
)


class ProviderType(TypedDict):
    id: str
    event: Event
    time: str
    play_standard_events: bool
    expected_can_play_timed_events: bool


providers: list[ProviderType] = [
    (
        {
            'id': 'An event can be played if the event time matches the current time',
            'event': {**default_event, 'time': 'Day'},
            'time': 'Day',
            'play_standard_events': False,
            'expected_can_play_timed_events': True,
        }
    ),
    (
        {
            'id': 'An event cannot be played if the event time does not match the current time',
            'event': {**default_event, 'time': 'Day'},
            'time': 'Night',
            'play_standard_events': False,
            'expected_can_play_timed_events': False,
        }
    ),
    (
        {
            'id': 'An event can be played if the event time is a list and the current time is in that list',
            'event': {**default_event, 'time': ['Day', 'Night']},
            'time': 'Night',
            'play_standard_events': False,
            'expected_can_play_timed_events': True,
        }
    ),
    (
        {
            'id': 'An event cannot be played if the event time is a list and the current time is not in that list',
            'event': {**default_event, 'time': ['Day', 'Night']},
            'time': 'Feast',
            'play_standard_events': False,
            'expected_can_play_timed_events': False,
        }
    ),
    (
        {
            'id': 'An event can be played if the event time is not specified and standard events are allowed',
            'event': default_event,
            'time': 'Day',
            'play_standard_events': True,
            'expected_can_play_timed_events': True,
        }
    ),
    (
        {
            'id': 'An event cannot be played if the event time is not specified and standard events are not allowed',
            'event': default_event,
            'time': 'Day',
            'play_standard_events': False,
            'expected_can_play_timed_events': False,
        }
    ),
]


@pytest.mark.parametrize('provider', providers, ids=lambda p: f'{p["id"]}')
def test_check_can_play_timed_events(provider: ProviderType):
    result = TimedEvents().can_play_event(
        provider['event'],
        {
            **default_game_round_state_without_event,
            'time': provider['time'],
            'play_standard_events': provider['play_standard_events'],
        },
    )

    assert result == provider['expected_can_play_timed_events']
