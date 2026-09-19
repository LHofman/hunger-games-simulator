import pytest

from typing import TypedDict

from Domain.EventRules.Groups import Groups
from Domain.types import Event, GameRoundStateWithoutEvent, Tribute
from tests.defaults import (
    defaultEvent,
    defaultGameOptions,
    defaultGameRoundStateWithoutEvent,
    defaultTribute
)


class ProviderType(TypedDict):
    id: str
    event: Event
    tribute: Tribute
    expectedCanBetrayTeammates: bool


providers: list[ProviderType] = [
    ({
        'id': 'An event without deaths can be played',
        'event': { **defaultEvent, 'name': 'Event without deaths' },
        'tribute': { **defaultTribute, },
        'expectedCanBetrayTeammates': True,
    }),
    ({
        'id': 'An event with deaths but no killTeammates can be played',
        'event': { **defaultEvent, 'deaths': ['Player2'] },
        'tribute': { **defaultTribute, },
        'expectedCanBetrayTeammates': True,
    }),
    ({
        'id': 'An event with deaths and killTeammates set to false can be played',
        'event': { **defaultEvent, 'deaths': ['Player2'], 'killTeammates': False },
        'tribute': { **defaultTribute, },
        'expectedCanBetrayTeammates': True,
    }),
    ({
        'id': 'An event killTeammates can be played if the tribute is not grouped with any other tributes',
        'event': { **defaultEvent, 'deaths': ['Player2'], 'killTeammates': True },
        'tribute': { **defaultTribute, 'groupedWith': [] },
        'expectedCanBetrayTeammates': True,
    }),
    ({
        'id': 'An event killTeammates can be played if the tribute is not grouped with the tribute that is killed',
        'event': { **defaultEvent, 'deaths': ['Player2'], 'killTeammates': True },
        'tribute': { **defaultTribute, 'groupedWith': ['Player3'] },
        'expectedCanBetrayTeammates': True,
    }),
    ({
        'id': 'An event killTeammates cannot be played if the tribute is grouped with the tribute that is killed',
        'event': { **defaultEvent, 'deaths': ['Player2'], 'killTeammates': True },
        'tribute': { **defaultTribute, 'groupedWith': ['Player2'] },
        'expectedCanBetrayTeammates': False,
    }),
]


@pytest.mark.parametrize('provider', providers, ids=lambda p: f'{p["id"]}')
def test_checkCanBetrayTeammates(provider: ProviderType):
    result = Groups().canPlayEvent(
        provider['event'],
        {
            **defaultGameRoundStateWithoutEvent,
            'currentTribute': provider['tribute']
        }
    )

    assert result == provider['expectedCanBetrayTeammates']


def test_canBetrayTeammatesIfOverriddenByOption():
    gameRoundState: GameRoundStateWithoutEvent = {
        **defaultGameRoundStateWithoutEvent,
        'options': {
            **defaultGameOptions,
            'betrayTeammates': True
        },
        'currentTribute': {
            **defaultTribute,
            'groupedWith': ['Player1', 'Player2']
        }
    }
    event: Event = {
        **defaultEvent,
        'deaths': ['Player1'],
        'killTeammates': True
    }
    result = Groups().canPlayEvent(event, gameRoundState)
    assert result == True
