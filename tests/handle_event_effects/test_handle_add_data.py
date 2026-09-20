from dataclasses import replace

from domain.event_rule import TextAndTerms
from domain.event_rules.tributes_data import TributesData
from domain.types import GameRoundState
from tests.defaults import (
    default_event,
    default_game_round_state,
    default_tribute,
)


def test_handle_add_data():
    game_state: GameRoundState = {
        **default_game_round_state,
        'event': {
            **default_event,
            'update_tributes_data': [
                {'tribute': 1, 'type': 'kills', 'operation': 'add', 'value': 1},
                {'tribute': 3, 'type': 'other', 'value': 2},
            ],
        },
        'tributes_alive': {
            'Tribute1': replace(default_tribute, name='Tribute1'),
            'Tribute2': replace(default_tribute, name='Tribute2'),
            'Tribute3': replace(default_tribute, name='Tribute3'),
        },
    }

    text_and_terms: TextAndTerms = {
        'text': '',
        'tributes': [
            replace(default_tribute, name='Tribute1'),
            replace(default_tribute, name='Tribute2'),
            replace(default_tribute, name='Tribute3'),
        ],
    }

    TributesData().handle_event_effects(
        game_state,
        text_and_terms,
    )

    assert game_state['tributes_data']['Tribute1']['kills'] == 1
    assert game_state['tributes_data']['Tribute3']['other'] == 2
