import pytest

from pytest_mock import MockerFixture
from typing import TypedDict

from domain.event_rules.groups import Groups
from domain.event_rule import TextAndTerms
from domain.types import Event, GameRoundState, GroupSizeType, Tribute
from tests.defaults import (
    default_event,
    default_game_round_state_without_event,
    default_tribute,
)


class ProviderType(TypedDict):
    id: str
    event: Event
    tribute: Tribute
    players_remaining: dict[str, Tribute]
    expected_text: str
    expected_players: list[Tribute]


@pytest.fixture(autouse=True)
def test_mock(mocker: MockerFixture):
    mocker.patch('random.random', return_value=0.5)
    mocker.patch(
        'random.choice',
        side_effect=lambda list: list[0], # type: ignore
    )


providers: list[ProviderType] = [
    ({
        'id': 'an event without require_group_size should not return any players',
        'event': {
            **default_event,
            'name': 'Event without require_group_size',
            'text': 'This is a test text with (Player1) and (Player2)',
        },
        'tribute': { **default_tribute, 'grouped_with': ['Player2', 'Player3'] },
        'players_remaining': {
            'Player3': { **default_tribute, 'name': 'Player3' },
        },
        'expected_text': 'This is a test text with Player1 and (Player2)',
        'expected_players': [
            { **default_tribute, 'grouped_with': ['Player2', 'Player3'] },
        ],
    }),
    ({
        'id': 'it should only return the players in the tribute\'s group that are still remaining',
        'event': {
            **default_event,
            'require_group_size': { 'type': GroupSizeType.EXACT, 'amount': 2 },
            'text': 'This is a test text with (Player1) and (Player2)',
        },
        'tribute': { **default_tribute, 'grouped_with': ['Player2', 'Player3'] },
        'players_remaining': {
            'Player3': { **default_tribute, 'name': 'Player3' },
        },
        'expected_text': 'This is a test text with Player1 and Player3',
        'expected_players': [
            { **default_tribute, 'grouped_with': ['Player2', 'Player3'] },
            { **default_tribute, 'name': 'Player3' },
        ],
    }),
    ({
        'id': 'it should return the correct group size and players when there are multiple players remaining',
        'event': {
            **default_event,
            'require_group_size': { 'type': GroupSizeType.EXACT, 'amount': 2 },
            'text': 'This is a test text with (Player1) and (Player2)',
        },
        'tribute': { **default_tribute, 'grouped_with': ['Player2', 'Player3'] },
        'players_remaining': {
            'Player2': { **default_tribute, 'name': 'Player2' },
            'Player3': { **default_tribute, 'name': 'Player3' },
        },
        'expected_text': 'This is a test text with Player1 and Player2',
        'expected_players': [
            { **default_tribute, 'grouped_with': ['Player2', 'Player3'] },
            { **default_tribute, 'name': 'Player2' },
        ],
    }),
]


@pytest.mark.parametrize('provider', providers, ids=lambda p: f'{p["id"]}')
def test_get_group_required_size_and_players(provider: ProviderType):
    game_state: GameRoundState = {
        **default_game_round_state_without_event,
        'event': provider['event'],
        'current_tribute': provider['tribute'],
        'players_remaining_this_round': provider['players_remaining']  ,
    }

    text_and_terms: TextAndTerms = {
        'text': provider['event']['text'].replace('(Player1)', 'Player1'),
        'players': [provider['tribute']],
    }

    result = Groups().replace_text_terms(
        game_state,
        text_and_terms,
    )

    assert result == {
        'text': provider['expected_text'],
        'players': provider['expected_players'],
    }
