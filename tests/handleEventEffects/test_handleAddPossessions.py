from Domain.EventRules.Possessions import Possessions
from Domain.EventRule import TextAndTerms
from Domain.types import GameRoundState
from tests.defaults import (
    defaultEvent,
    defaultGameRoundState,
    defaultTribute,
)


def test_handleAddPossessions():
    gameState: GameRoundState = {
        **defaultGameRoundState,
        'event': {
            **defaultEvent,
            'addPossessions': [
                { 'player': 1, 'type': 'item', 'value': 'bow' },
                { 'player': 3, 'type': 'pet', 'value': '(Animal1)' },
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
        ],
        'terms': {
            '(Animal1)': 'cat'
        }
    }

    Possessions().handleEventEffects(
        gameState,
        textAndTerms
    )

    assert gameState['playersAlive']['Tribute1']['possessions']['item'] == ['bow']
    assert gameState['playersAlive']['Tribute3']['possessions']['pet'] == ['cat']