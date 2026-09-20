from dataclasses import replace

from domain.event_rule import TextAndTerms
from domain.event_rules.deaths import Deaths
from domain.types import GameRoundState
from tests.defaults import (
    default_event,
    default_game_round_state,
    default_tribute,
)


def test_handle_deaths():
    tributes = {
        'Tribute1': replace(
            default_tribute,
            name='Tribute1',
            district=1,
            grouped_with=['Tribute2', 'Tribute3'],
        ),
        'Tribute2': replace(
            default_tribute,
            name='Tribute2',
            district=2,
            grouped_with=['Tribute1'],
        ),
        'Tribute3': replace(
            default_tribute,
            name='Tribute3',
            district=3,
            grouped_with=['Tribute1'],
        ),
    }

    game_state: GameRoundState = {
        **default_game_round_state,
        'event': {
            **default_event,
            'deaths': ['Tribute2', 'Tribute3'],
            'add_kills': [{'tribute': 1, 'value': 2}],
        },
        'all_tributes': tributes.copy(),
        'tributes_alive': tributes.copy(),
        'exact_time': 'day',
    }

    text_and_terms: TextAndTerms = {
        'text': '',
        'tributes': list(tributes.values()),
    }

    Deaths().handle_event_effects(
        game_state,
        text_and_terms,
    )

    assert game_state['recent_deaths'] == ['Tribute2', 'Tribute3']
    assert game_state['all_tributes']['Tribute2'].time_of_death == 'day'
    assert game_state['all_tributes']['Tribute3'].time_of_death == 'day'
    assert game_state['tributes_alive'] == {
        'Tribute1': replace(
            default_tribute,
            name='Tribute1',
            district=1,
            grouped_with=[],
            kills=2,
        ),
    }
