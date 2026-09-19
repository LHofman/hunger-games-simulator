import pytest

from pytest_mock import MockerFixture

from Domain.EventRules.Possessions import Possessions
from Domain.EventRule import TextAndTerms
from Domain.types import GameRoundState
from tests.defaults import (
    defaultGameRoundState,
    defaultTribute,
)


@pytest.fixture(autouse=True)
def test_mock(mocker: MockerFixture):
    mocker.patch(
        'random.choice',
        side_effect=lambda list: list[0], # type: ignore
    )


def test_setPossessionsTerms():
    gameState: GameRoundState = {
        **defaultGameRoundState,
        'currentTribute': {
            **defaultTribute,
            'possessions': { 'pet': ['cat', 'dog'] },
        },
    }

    textAndTerms: TextAndTerms = {
        'text': 'Tribute\'s pet (Possession:pet1) attacks and kills Enemy.',
    }

    result = Possessions().replaceTextTerms(
        gameState,
        textAndTerms,
    )

    assert result == {
        'text': 'Tribute\'s pet cat attacks and kills Enemy.',
        'terms': { '(Possession:pet1)': 'cat' },
    }
