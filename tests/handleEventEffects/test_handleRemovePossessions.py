from Domain.EventRules.Possessions import Possessions
from Domain.EventRule import TextAndTerms
from Domain.types import GameRoundState
from tests.defaults import (
    defaultEvent,
    defaultGameRoundState,
    defaultTribute,
)

def test_handleRemovePossessions():
    gameState: GameRoundState = {
        **defaultGameRoundState,
        'event': {
            **defaultEvent,
            'removePossessions': [
                { 'player': 1, 'type': 'item', 'value': 'bow' },
                { 'player': 3, 'type': 'pet', 'value': '(Animal1)' },
            ]
        },
        'playersAlive': {
            'Tribute1': { **defaultTribute, 'name': 'Tribute1', 'possessions': { 'item': ['bow', 'sword'], 'pet': ['cat'] } },
            'Tribute2': { **defaultTribute, 'name': 'Tribute2', 'possessions': { 'pet': ['cat', 'dog'] } },
            'Tribute3': { **defaultTribute, 'name': 'Tribute3', 'possessions': { 'item': ['bow', 'sword'], 'pet': ['cat', 'dog'] } },
        }
    }

    textAndTerms: TextAndTerms = {
        'text': '',
        'players': [
            { **defaultTribute, 'name': 'Tribute1', 'possessions': { 'item': ['bow', 'sword'], 'pet': ['cat'] } },
            { **defaultTribute, 'name': 'Tribute2', 'possessions': { 'pet': ['cat', 'dog'] } },
            { **defaultTribute, 'name': 'Tribute3', 'possessions': { 'item': ['bow', 'sword'], 'pet': ['cat', 'dog'] } },
        ],
        'terms': {
            '(Animal1)': 'cat'
        }
    }

    Possessions().handleEventEffects(
        gameState,
        textAndTerms
    )

    assert gameState['playersAlive']['Tribute1']['possessions'] == { 'item': ['sword'], 'pet': ['cat'] }
    assert gameState['playersAlive']['Tribute2']['possessions'] == { 'pet': ['cat', 'dog'] }
    assert gameState['playersAlive']['Tribute3']['possessions'] == { 'item': ['bow', 'sword'], 'pet': ['dog'] }
