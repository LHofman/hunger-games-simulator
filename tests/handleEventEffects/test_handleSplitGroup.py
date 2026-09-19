from Domain.EventRules.Groups import Groups
from Domain.EventRule import TextAndTerms
from Domain.types import GameRoundState
from tests.defaults import (
    defaultEvent,
    defaultGameRoundState,
    defaultTribute,
)


def test_handleSplitGroup():
    gameState: GameRoundState = {
        **defaultGameRoundState,
        'event': {
            **defaultEvent,
            'splitGroup': ['Player1', 'Player2'],
        },
        'playersAlive': {
            'Tribute1': {
                **defaultTribute,
                'name': 'Tribute1',
                'groupedWith': ['Tribute2'],
            },
            'Tribute2': {
                **defaultTribute,
                'name': 'Tribute2',
                'groupedWith': ['Tribute1'],
            },
            'Tribute3': {
                **defaultTribute,
                'name': 'Tribute3',
                'groupedWith': ['Tribute4'],
            },
            'Tribute4': {
                **defaultTribute,
                'name': 'Tribute4',
                'groupedWith': ['Tribute3'],
            },
        },
    }

    textAndTerms: TextAndTerms = {
        'text': '',
        'players': [
            { **defaultTribute, 'name': 'Tribute1' },
            { **defaultTribute, 'name': 'Tribute2' },
        ],
    }

    Groups().handleEventEffects(
        gameState,
        textAndTerms,
    )

    assert gameState['playersAlive']['Tribute1']['groupedWith'] == []
    assert gameState['playersAlive']['Tribute2']['groupedWith'] == []
    assert gameState['playersAlive']['Tribute3']['groupedWith'] == ['Tribute4']
    assert gameState['playersAlive']['Tribute4']['groupedWith'] == ['Tribute3']