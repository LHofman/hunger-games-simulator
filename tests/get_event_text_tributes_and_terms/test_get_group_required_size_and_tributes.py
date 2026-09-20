from dataclasses import replace
from typing import TypedDict

import pytest
from pytest_mock import MockerFixture

from domain.event_rule import TextAndTerms
from domain.event_rules.groups import Groups
from domain.tribute import Tribute
from domain.types import Event, GameRoundState, GroupSizeType
from tests.defaults import (
    default_event,
    default_game_round_state_without_event,
    default_tribute,
)


class ProviderType(TypedDict):
    id: str
    event: Event
    tribute: Tribute
    tributes_remaining: dict[str, Tribute]
    expected_text: str
    expected_tributes: list[Tribute]


@pytest.fixture(autouse=True)
def test_mock(mocker: MockerFixture):
    mocker.patch('random.random', return_value=0.5)
    mocker.patch(
        'random.choice',
        side_effect=lambda list: list[0],  # type: ignore
    )


providers: list[ProviderType] = [
    (
        {
            'id': 'an event without require_group_size should not return any tributes',
            'event': {
                **default_event,
                'name': 'Event without require_group_size',
                'text': 'This is a test text with (Tribute1) and (Tribute2)',
            },
            'tribute': replace(
                default_tribute,
                grouped_with=['Tribute2', 'Tribute3'],
            ),
            'tributes_remaining': {
                'Tribute3': replace(default_tribute, name='Tribute3'),
            },
            'expected_text': 'This is a test text with Tribute1 and (Tribute2)',
            'expected_tributes': [
                replace(
                    default_tribute,
                    grouped_with=['Tribute2', 'Tribute3'],
                ),
            ],
        }
    ),
    (
        {
            'id': "it should only return the tributes in the tribute's group that are still remaining",
            'event': {
                **default_event,
                'require_group_size': {
                    'type': GroupSizeType.EXACT,
                    'amount': 2,
                },
                'text': 'This is a test text with (Tribute1) and (Tribute2)',
            },
            'tribute': replace(
                default_tribute,
                grouped_with=['Tribute2', 'Tribute3'],
            ),
            'tributes_remaining': {
                'Tribute3': replace(default_tribute, name='Tribute3'),
            },
            'expected_text': 'This is a test text with Tribute1 and Tribute3',
            'expected_tributes': [
                replace(
                    default_tribute,
                    grouped_with=['Tribute2', 'Tribute3'],
                ),
                replace(default_tribute, name='Tribute3'),
            ],
        }
    ),
    (
        {
            'id': 'it should return the correct group size and tributes when there are multiple tributes remaining',
            'event': {
                **default_event,
                'require_group_size': {
                    'type': GroupSizeType.EXACT,
                    'amount': 2,
                },
                'text': 'This is a test text with (Tribute1) and (Tribute2)',
            },
            'tribute': replace(
                default_tribute,
                grouped_with=['Tribute2', 'Tribute3'],
            ),
            'tributes_remaining': {
                'Tribute2': replace(default_tribute, name='Tribute2'),
                'Tribute3': replace(default_tribute, name='Tribute3'),
            },
            'expected_text': 'This is a test text with Tribute1 and Tribute2',
            'expected_tributes': [
                replace(
                    default_tribute,
                    grouped_with=['Tribute2', 'Tribute3'],
                ),
                replace(default_tribute, name='Tribute2'),
            ],
        }
    ),
]


@pytest.mark.parametrize('provider', providers, ids=lambda p: f'{p["id"]}')
def test_get_group_required_size_and_tributes(provider: ProviderType):
    game_state: GameRoundState = {
        **default_game_round_state_without_event,
        'event': provider['event'],
        'current_tribute': provider['tribute'],
        'tributes_remaining_this_round': provider['tributes_remaining'],
    }

    text_and_terms: TextAndTerms = {
        'text': provider['event']['text'].replace('(Tribute1)', 'Tribute1'),
        'tributes': [provider['tribute']],
    }

    result = Groups().replace_text_terms(
        game_state,
        text_and_terms,
    )

    assert result == {
        'text': provider['expected_text'],
        'tributes': provider['expected_tributes'],
    }
