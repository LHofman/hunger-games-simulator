import pytest
from pytest_mock import MockerFixture

from domain.event_rule import TextAndTerms
from domain.event_rules.other_terms import OtherTerms
from domain.types import GameRoundState
from tests.defaults import (
    default_game_round_state,
)


@pytest.fixture(autouse=True)
def test_mock(mocker: MockerFixture):
    mocker.patch(
        'random.choice',
        side_effect=lambda list: list[0],  # type: ignore
    )


def test_setother_terms():
    game_state: GameRoundState = {
        **default_game_round_state,
        'other_terms': {'Animal': ['cat', 'dog']},
    }

    text_and_terms: TextAndTerms = {
        'text': 'Tribute finds a (Animal1), They pet it and the (Animal1) follows them around',
    }

    result = OtherTerms().replace_text_terms(
        game_state,
        text_and_terms,
    )

    assert result == {
        'text': 'Tribute finds a cat, They pet it and the cat follows them around',
        'terms': {'(Animal1)': 'cat'},
    }
