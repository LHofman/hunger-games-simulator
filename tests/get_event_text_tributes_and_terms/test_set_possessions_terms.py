from dataclasses import replace

import pytest
from pytest_mock import MockerFixture

from domain.event_rule import TextAndTerms
from domain.event_rules.possessions import Possessions
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


def test_set_possessions_terms():
    game_state: GameRoundState = {
        **default_game_round_state,
        'current_tribute': replace(
            default_tribute,
            possessions={'pet': ['cat', 'dog']},
        ),
    }

    text_and_terms: TextAndTerms = {
        'text': "Tribute's pet (Possession:pet1) attacks and kills Enemy.",
    }

    result = Possessions().replace_text_terms(
        game_state,
        text_and_terms,
    )

    assert result == {
        'text': "Tribute's pet cat attacks and kills Enemy.",
        'terms': {'(Possession:pet1)': 'cat'},
    }
