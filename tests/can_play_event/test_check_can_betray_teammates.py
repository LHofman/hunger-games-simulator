import pytest

from typing import TypedDict

from domain.event_rules.groups import Groups
from domain.types import Event, GameRoundStateWithoutEvent, Tribute
from tests.defaults import (
    default_event,
    default_game_options,
    default_game_round_state_without_event,
    default_tribute,
)


class ProviderType(TypedDict):
    id: str
    event: Event
    tribute: Tribute
    expected_can_betray_teammates: bool


providers: list[ProviderType] = [
    ({
        'id': 'An event without deaths can be played',
        'event': { **default_event, 'name': 'Event without deaths' },
        'tribute': { **default_tribute, },
        'expected_can_betray_teammates': True,
    }),
    ({
        'id': 'An event with deaths but no kill_teammates can be played',
        'event': { **default_event, 'deaths': ['Player2'] },
        'tribute': { **default_tribute, },
        'expected_can_betray_teammates': True,
    }),
    ({
        'id': 'An event with deaths and kill_teammates set to false can be played',
        'event': { **default_event, 'deaths': ['Player2'], 'kill_teammates': False },
        'tribute': { **default_tribute, },
        'expected_can_betray_teammates': True,
    }),
    ({
        'id': 'An event kill_teammates can be played if the tribute is not grouped with any other tributes',
        'event': { **default_event, 'deaths': ['Player2'], 'kill_teammates': True },
        'tribute': { **default_tribute, 'grouped_with': [] },
        'expected_can_betray_teammates': True,
    }),
    ({
        'id': 'An event kill_teammates can be played if the tribute is not grouped with the tribute that is killed',
        'event': { **default_event, 'deaths': ['Player2'], 'kill_teammates': True },
        'tribute': { **default_tribute, 'grouped_with': ['Player3'] },
        'expected_can_betray_teammates': True,
    }),
    ({
        'id': 'An event kill_teammates cannot be played if the tribute is grouped with the tribute that is killed',
        'event': { **default_event, 'deaths': ['Player2'], 'kill_teammates': True },
        'tribute': { **default_tribute, 'grouped_with': ['Player2'] },
        'expected_can_betray_teammates': False,
    }),
]


@pytest.mark.parametrize('provider', providers, ids=lambda p: f'{p["id"]}')
def test_check_can_betray_teammates(provider: ProviderType):
    result = Groups().can_play_event(
        provider['event'],
        {
            **default_game_round_state_without_event,
            'current_tribute': provider['tribute'],
        },
    )

    assert result == provider['expected_can_betray_teammates']


def test_can_betray_teammates_if_overridden_by_option():
    game_round_state: GameRoundStateWithoutEvent = {
        **default_game_round_state_without_event,
        'options': {
            **default_game_options,
            'betray_teammates': True,
        },
        'current_tribute': {
            **default_tribute,
            'grouped_with': ['Player1', 'Player2'],
        },
    }
    event: Event = {
        **default_event,
        'deaths': ['Player1'],
        'kill_teammates': True,
    }
    result = Groups().can_play_event(event, game_round_state)
    assert result == True
