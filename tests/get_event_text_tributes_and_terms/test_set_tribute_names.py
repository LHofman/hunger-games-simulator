from dataclasses import replace

import pytest
from pytest_mock import MockerFixture

from domain.event_rule import TextAndTerms
from domain.event_rules.multiple_tributes import MultipleTributes
from domain.types import GameRoundState
from tests.defaults import (
    default_game_round_state,
    default_tribute,
)


@pytest.fixture(autouse=True)
def test_mock(mocker: MockerFixture):
    mocker.patch(
        'random.choice',
        side_effect=lambda list: list[0],  # type: ignore
    )


def test_set_tributes_names():
    game_state: GameRoundState = {
        **default_game_round_state,
        'tributes_remaining_this_round': {
            'Enemy': replace(default_tribute, name='Enemy'),
            'Enemy 2': replace(default_tribute, name='Enemy 2'),
        },
    }

    text_and_terms: TextAndTerms = {
        'text': 'Tribute1 is working with Friend to kill (Tribute3) and (Tribute4)',
        'tributes': [
            replace(default_tribute, name='Tribute1'),
            replace(default_tribute, name='Friend'),
        ],
    }

    result = MultipleTributes().replace_text_terms(
        game_state,
        text_and_terms,
    )

    assert result == {
        'text': 'Tribute1 is working with Friend to kill Enemy and Enemy 2',
        'tributes': [
            replace(default_tribute, name='Tribute1'),
            replace(default_tribute, name='Friend'),
            replace(default_tribute, name='Enemy'),
            replace(default_tribute, name='Enemy 2'),
        ],
    }
