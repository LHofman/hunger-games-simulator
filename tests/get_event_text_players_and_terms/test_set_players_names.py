import pytest

from pytest_mock import MockerFixture

from domain.event_rules.multiple_players import MultiplePlayers
from domain.event_rule import TextAndTerms
from domain.types import GameRoundState
from tests.defaults import (
    default_game_round_state,
    default_tribute,
)


@pytest.fixture(autouse=True)
def test_mock(mocker: MockerFixture):
    mocker.patch(
        'random.choice',
        side_effect=lambda list: list[0], # type: ignore
    )


def test_set_players_names():
    game_state: GameRoundState = {
        **default_game_round_state,
        'players_remaining_this_round': {
            'Enemy': { **default_tribute, 'name': 'Enemy' },
            'Enemy 2': { **default_tribute, 'name': 'Enemy 2' },
        },
    }

    text_and_terms: TextAndTerms = {
        'text': 'Player1 is working with Friend to kill (Player3) and (Player4)',
        'players': [
            { **default_tribute, 'name': 'Player1' },
            { **default_tribute, 'name': 'Friend' },
        ],
    }

    result = MultiplePlayers().replace_text_terms(
        game_state,
        text_and_terms,
    )

    assert result == {
        'text': 'Player1 is working with Friend to kill Enemy and Enemy 2',
        'players': [
            { **default_tribute, 'name': 'Player1' },
            { **default_tribute, 'name': 'Friend' },
            { **default_tribute, 'name': 'Enemy' },
            { **default_tribute, 'name': 'Enemy 2' },
        ],
    }
