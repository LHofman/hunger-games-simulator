import pytest

from pytest_mock import MockerFixture

from Domain.EventRules.MultiplePlayers import MultiplePlayers
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


def test_setPlayersNames():
    gameState: GameRoundState = {
        **defaultGameRoundState,
        'playersRemainingThisRound': {
            'Enemy': { **defaultTribute, 'name': 'Enemy' },
            'Enemy 2': { **defaultTribute, 'name': 'Enemy 2' },
        },
    }

    textAndTerms: TextAndTerms = {
        'text': 'Player1 is working with Friend to kill (Player3) and (Player4)',
        'players': [
            { **defaultTribute, 'name': 'Player1' },
            { **defaultTribute, 'name': 'Friend' },
        ],
    }

    result = MultiplePlayers().replaceTextTerms(
        gameState,
        textAndTerms,
    )

    assert result == {
        'text': 'Player1 is working with Friend to kill Enemy and Enemy 2',
        'players': [
            { **defaultTribute, 'name': 'Player1' },
            { **defaultTribute, 'name': 'Friend' },
            { **defaultTribute, 'name': 'Enemy' },
            { **defaultTribute, 'name': 'Enemy 2' },
        ],
    }
