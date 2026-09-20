from domain.event_rule import TextAndTerms
from domain.event_rules.possessions import Possessions
from domain.types import GameRoundState
from tests.defaults import (
    default_event,
    default_game_round_state,
    default_tribute,
)


def test_handleadd_possessions():
    game_state: GameRoundState = {
        **default_game_round_state,
        'event': {
            **default_event,
            'add_possessions': [
                {'tribute': 1, 'type': 'item', 'value': 'bow'},
                {'tribute': 3, 'type': 'pet', 'value': '(Animal1)'},
            ],
        },
        'tributes_alive': {
            'Tribute1': {**default_tribute, 'name': 'Tribute1'},
            'Tribute2': {**default_tribute, 'name': 'Tribute2'},
            'Tribute3': {**default_tribute, 'name': 'Tribute3'},
        },
    }

    text_and_terms: TextAndTerms = {
        'text': '',
        'tributes': [
            {**default_tribute, 'name': 'Tribute1'},
            {**default_tribute, 'name': 'Tribute2'},
            {**default_tribute, 'name': 'Tribute3'},
        ],
        'terms': {
            '(Animal1)': 'cat',
        },
    }

    Possessions().handle_event_effects(
        game_state,
        text_and_terms,
    )

    assert game_state['tributes_alive']['Tribute1']['possessions']['item'] == [
        'bow'
    ]
    assert game_state['tributes_alive']['Tribute3']['possessions']['pet'] == [
        'cat'
    ]
