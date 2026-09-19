import pytest

from typing import TypedDict

from Domain.EventRules.TimedEvents import TimedEvents
from Domain.types import Event
from tests.defaults import (
    defaultEvent,
    defaultGameRoundStateWithoutEvent,
)


class ProviderType(TypedDict):
    id: str
    event: Event
    time: str
    playStandardEvents: bool
    expectedCanPlayTimedEvents: bool


providers: list[ProviderType] = [
    ({
        'id': 'An event can be played if the event time matches the current time',
        'event': { **defaultEvent, 'time': 'Day' },
        'time': 'Day',
        'playStandardEvents': False,
        'expectedCanPlayTimedEvents': True,
    }),
    ({
        'id': 'An event cannot be played if the event time does not match the current time',
        'event': { **defaultEvent, 'time': 'Day' },
        'time': 'Night',
        'playStandardEvents': False,
        'expectedCanPlayTimedEvents': False,
    }),
    ({
        'id': 'An event can be played if the event time is a list and the current time is in that list',
        'event': { **defaultEvent, 'time': ['Day', 'Night'] },
        'time': 'Night',
        'playStandardEvents': False,
        'expectedCanPlayTimedEvents': True,
    }),
    ({
        'id': 'An event cannot be played if the event time is a list and the current time is not in that list',
        'event': { **defaultEvent, 'time': ['Day', 'Night'] },
        'time': 'Feast',
        'playStandardEvents': False,
        'expectedCanPlayTimedEvents': False,
    }),
    ({
        'id': 'An event can be played if the event time is not specified and standard events are allowed',
        'event': defaultEvent,
        'time': 'Day',
        'playStandardEvents': True,
        'expectedCanPlayTimedEvents': True,
    }),
    ({
        'id': 'An event cannot be played if the event time is not specified and standard events are not allowed',
        'event': defaultEvent,
        'time': 'Day',
        'playStandardEvents': False,
        'expectedCanPlayTimedEvents': False,
    }),
]


@pytest.mark.parametrize('provider', providers, ids=lambda p: f'{p["id"]}')
def test_checkCanPlayTimedEvents(provider: ProviderType):
    result = TimedEvents().canPlayEvent(
        provider['event'],
        {
            **defaultGameRoundStateWithoutEvent,
            'time': provider['time'],
            'playStandardEvents': provider['playStandardEvents'],
        }
    )
    
    assert result == provider['expectedCanPlayTimedEvents']
