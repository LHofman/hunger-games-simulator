from domain.event_rules.groups import Groups
from domain.event_rule import TextAndTerms
from domain.types import GameRoundState
from tests.defaults import (
    default_event,
    default_game_round_state,
    default_tribute,
)


def test_handleform_group():
    game_state: GameRoundState = {
        **default_game_round_state,
        'event': {
            **default_event,
            'form_group': ['Player1', 'Player2'],
        },
        'players_alive': {
            'Tribute1': {
                **default_tribute,
                'name': 'Tribute1',
                'grouped_with': [],
            },
            'Tribute2': {
                **default_tribute,
                'name': 'Tribute2',
                'grouped_with': [],
            },
            'Tribute3': {
                **default_tribute,
                'name': 'Tribute3',
                'grouped_with': [],
            },
        },
    }

    text_and_terms: TextAndTerms = {
        'text': '',
        'players': [
            { **default_tribute, 'name': 'Tribute1' },
            { **default_tribute, 'name': 'Tribute2' },
        ],
    }

    Groups().handle_event_effects(
        game_state,
        text_and_terms,
    )

    assert game_state['players_alive']['Tribute1']['grouped_with'] == ['Tribute2']
    assert game_state['players_alive']['Tribute2']['grouped_with'] == ['Tribute1']
    assert game_state['players_alive']['Tribute3']['grouped_with'] == []