from dataclasses import replace

from domain.event_rule import TextAndTerms
from domain.event_rules.groups import Groups
from domain.types import GameRoundState
from tests.defaults import (
    default_event,
    default_game_round_state,
    default_tribute,
)


def test_handlesplit_group():
    game_state: GameRoundState = {
        **default_game_round_state,
        'event': {
            **default_event,
            'split_group': ['Tribute1', 'Tribute2'],
        },
        'tributes_alive': {
            'Tribute1': replace(
                default_tribute,
                name='Tribute1',
                grouped_with=['Tribute2'],
            ),
            'Tribute2': replace(
                default_tribute,
                name='Tribute2',
                grouped_with=['Tribute1'],
            ),
            'Tribute3': replace(
                default_tribute,
                name='Tribute3',
                grouped_with=['Tribute4'],
            ),
            'Tribute4': replace(
                default_tribute,
                name='Tribute4',
                grouped_with=['Tribute3'],
            ),
        },
    }

    text_and_terms: TextAndTerms = {
        'text': '',
        'tributes': [
            replace(
                default_tribute,
                name='Tribute1',
                grouped_with=['Tribute2'],
            ),
            replace(
                default_tribute,
                name='Tribute2',
                grouped_with=['Tribute1'],
            ),
        ],
    }

    Groups().handle_event_effects(
        game_state,
        text_and_terms,
    )

    assert game_state['tributes_alive']['Tribute1'].grouped_with == []
    assert game_state['tributes_alive']['Tribute2'].grouped_with == []
    assert game_state['tributes_alive']['Tribute3'].grouped_with == ['Tribute4']
    assert game_state['tributes_alive']['Tribute4'].grouped_with == ['Tribute3']
