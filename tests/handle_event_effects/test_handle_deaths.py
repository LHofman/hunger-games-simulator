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
    game_state: GameRoundState = {
        **default_game_round_state,
        'event': {
            **default_event,
            'deaths': ['Tribute2', 'Tribute3'],
        },
        'tributes_alive': {
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
        },
        'exact_time': 'day',
    }

    text_and_terms: TextAndTerms = {
        'text': '',
        'tributes': [
            replace(
                default_tribute,
                name='Tribute1',
                district=1,
                grouped_with=['Tribute2', 'Tribute3'],
            ),
            replace(
                default_tribute,
                name='Tribute2',
                district=2,
                grouped_with=['Tribute1'],
            ),
            replace(
                default_tribute,
                name='Tribute3',
                district=3,
                grouped_with=['Tribute1'],
            ),
        ],
    }

    Deaths().handle_event_effects(
        game_state,
        text_and_terms,
    )

    assert game_state['recent_deaths'] == [('Tribute2', 2), ('Tribute3', 3)]
    assert game_state['tributes_data']['Tribute2']['time of death'] == 'day'
    assert game_state['tributes_data']['Tribute2']['district'] == 2  #  type: ignore
    assert game_state['tributes_data']['Tribute3']['time of death'] == 'day'
    assert game_state['tributes_data']['Tribute3']['district'] == 3  #  type: ignore
    assert game_state['tributes_alive'] == {
        'Tribute1': replace(
            default_tribute,
            name='Tribute1',
            district=1,
            grouped_with=[],
        ),
    }
