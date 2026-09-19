from typing import TypedDict
import pytest
from pytest_mock import MockerFixture
from Domain.EventRules.Groups import Groups
from Domain.EventRule import TextAndTerms
from Domain.types import Event, GameRoundState, GroupSizeType, Tribute
from tests.defaults import (
    defaultEvent,
    defaultGameRoundStateWithoutEvent,
    defaultTribute,
)

class ProviderType(TypedDict):
    id: str
    event: Event
    tribute: Tribute
    playersRemaining: dict[str, Tribute]
    expectedText: str
    expectedPlayers: list[Tribute]

@pytest.fixture(autouse=True)
def test_mock(mocker: MockerFixture):
    mocker.patch( 'random.random', return_value=0.5 )
    mocker.patch(
        'random.choice',
        side_effect=lambda list: list[0] # type: ignore
    )

providers: list[ProviderType] = [
    ({
        'id': 'an event without requireGroupSize should not return any players',
        'event': {
            **defaultEvent,
            'name': 'Event without requireGroupSize',
            'text': 'This is a test text with (Player1) and (Player2)',
        },
        'tribute': { **defaultTribute, 'groupedWith': ['Player2', 'Player3'] },
        'playersRemaining': {
            'Player3': { **defaultTribute, 'name': 'Player3' }
        },
        'expectedText': 'This is a test text with Player1 and (Player2)',
        'expectedPlayers': [
            { **defaultTribute, 'groupedWith': ['Player2', 'Player3'] }
        ]
    }),
    ({
        'id': 'it should only return the players in the tribute\'s group that are still remaining',
        'event': {
            **defaultEvent,
            'requireGroupSize': { 'type': GroupSizeType.EXACT, 'amount': 2 },
            'text': 'This is a test text with (Player1) and (Player2)',
        },
        'tribute': { **defaultTribute, 'groupedWith': ['Player2', 'Player3'] },
        'playersRemaining': {
            'Player3': { **defaultTribute, 'name': 'Player3' }
        },
        'expectedText': 'This is a test text with Player1 and Player3',
        'expectedPlayers': [
            { **defaultTribute, 'groupedWith': ['Player2', 'Player3'] },
            { **defaultTribute, 'name': 'Player3' }
        ]
    }),
    ({
        'id': 'it should return the correct group size and players when there are multiple players remaining',
        'event': {
            **defaultEvent,
            'requireGroupSize': { 'type': GroupSizeType.EXACT, 'amount': 2 },
            'text': 'This is a test text with (Player1) and (Player2)',
        },
        'tribute': { **defaultTribute, 'groupedWith': ['Player2', 'Player3'] },
        'playersRemaining': {
            'Player2': { **defaultTribute, 'name': 'Player2' },
            'Player3': { **defaultTribute, 'name': 'Player3' }
        },
        'expectedText': 'This is a test text with Player1 and Player2',
        'expectedPlayers': [
            { **defaultTribute, 'groupedWith': ['Player2', 'Player3'] },
            { **defaultTribute, 'name': 'Player2' }
        ],
    }),
]

@pytest.mark.parametrize('provider', providers, ids=lambda p: f'{p["id"]}')
def test_getGroupRequiredSizeAndPlayers(provider: ProviderType):
    gameState: GameRoundState = {
        **defaultGameRoundStateWithoutEvent,
        'event': provider['event'],
        'currentTribute': provider['tribute'],
        'playersRemainingThisRound': provider['playersRemaining']  
    }

    textAndTerms: TextAndTerms = {
        'text': provider['event']['text'].replace('(Player1)', 'Player1'),
        'players': [provider['tribute']]
    }

    result = Groups().replaceTextTerms(
        gameState,
        textAndTerms,
    )

    assert result == {
        'text': provider['expectedText'],
        'players': provider['expectedPlayers']
    }
