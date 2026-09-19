from Domain.EventRules.TributesData import TributesData
from Domain.EventRule import TextAndTerms
from Domain.types import GameRoundState
from tests.defaults import (
    defaultEvent,
    defaultGameRoundState,
    defaultTribute,
)


def test_handleAddData():
    gameState: GameRoundState = {
        **defaultGameRoundState,
        'event': {
            **defaultEvent,
            'updateTributesData': [
                { 'player': 1, 'type': 'kills', 'operation': 'add', 'value': 1 },
                { 'player': 3, 'type': 'other', 'value': 2 },
            ]
        },
        'playersAlive': {
            'Tribute1': { **defaultTribute, 'name': 'Tribute1' },
            'Tribute2': { **defaultTribute, 'name': 'Tribute2' },
            'Tribute3': { **defaultTribute, 'name': 'Tribute3' },
        }
    }

    textAndTerms: TextAndTerms = {
        'text': '',
        'players': [
            { **defaultTribute, 'name': 'Tribute1' },
            { **defaultTribute, 'name': 'Tribute2' },
            { **defaultTribute, 'name': 'Tribute3' },
        ]
    }

    TributesData().handleEventEffects(
        gameState,
        textAndTerms
    )

    assert gameState['tributesData']['Tribute1']['kills'] == 1
    assert gameState['tributesData']['Tribute3']['other'] == 2
