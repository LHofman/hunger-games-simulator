from typing import TypedDict

import pytest
from pytest_mock import MockerFixture

from domain.event_rule import TextAndTerms
from domain.event_rules.sponsors import Sponsors
from domain.types import GameRoundState, Tribute
from tests.defaults import (
    default_game_options,
    default_game_round_state,
    default_tribute,
)


class ProviderType(TypedDict):
    id: str
    text: str
    one_sponsor_per_tribute: bool
    tribute: Tribute
    sponsors: list[str]
    expected_text: str


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
            'id': "Text without (Sponsor) placeholder doesn't change.",
            'text': 'Tribute explores the arena.',
            'one_sponsor_per_tribute': True,
            'tribute': {**default_tribute, 'index': 2},
            'sponsors': ['Sponsor1', 'Sponsor2'],
            'expected_text': 'Tribute explores the arena.',
        }
    ),
    (
        {
            'id': 'If the option one_sponsor_per_tribute is disabled, a random sponsor is chosen',
            'text': 'Tribute receives a bow, some arrows, and a quiver from (Sponsor).',
            'one_sponsor_per_tribute': False,
            'tribute': {**default_tribute, 'index': 2},
            'sponsors': ['Sponsor1', 'Sponsor2'],
            'expected_text': 'Tribute receives a bow, some arrows, and a quiver from Sponsor1.',
        }
    ),
    (
        {
            'id': 'If there are more sponsors than tributes, a random sponsor is chosen',
            'text': 'Tribute receives a bow, some arrows, and a quiver from (Sponsor).',
            'one_sponsor_per_tribute': True,
            'tribute': {**default_tribute, 'index': 2},
            'sponsors': ['Sponsor1', 'Sponsor2', 'Sponsor3'],
            'expected_text': 'Tribute receives a bow, some arrows, and a quiver from Sponsor1.',
        }
    ),
    (
        {
            'id': 'If there are less sponsors than tributes, a random sponsor is chosen',
            'text': 'Tribute receives a bow, some arrows, and a quiver from (Sponsor).',
            'one_sponsor_per_tribute': True,
            'tribute': {**default_tribute, 'index': 2},
            'sponsors': ['Sponsor3'],
            'expected_text': 'Tribute receives a bow, some arrows, and a quiver from Sponsor3.',
        }
    ),
    (
        {
            'id': 'A tribute receives an item from their respective sponsor',
            'text': 'Tribute receives a bow, some arrows, and a quiver from (Sponsor).',
            'one_sponsor_per_tribute': True,
            'tribute': {**default_tribute, 'index': 2},
            'sponsors': ['Sponsor1', 'Sponsor2'],
            'expected_text': 'Tribute receives a bow, some arrows, and a quiver from Sponsor2.',
        }
    ),
    (
        {
            'id': 'A tribute receives an item from an opposing sponsor',
            'text': 'Tribute receives a bow, some arrows, and a quiver from (Sponsor::opposing).',
            'one_sponsor_per_tribute': True,
            'tribute': {**default_tribute, 'index': 2},
            'sponsors': ['Sponsor1', 'Sponsor2'],
            'expected_text': 'Tribute receives a bow, some arrows, and a quiver from Sponsor1.',
        }
    ),
]


@pytest.mark.parametrize('provider', providers, ids=lambda p: f'{p["id"]}')
def test_set_sponsors_names(provider: ProviderType):
    game_state: GameRoundState = {
        **default_game_round_state,
        'total_tributes': 2,
        'options': {
            **default_game_options,
            'one_sponsor_per_tribute': provider['one_sponsor_per_tribute'],
        },
        'current_tribute': provider['tribute'],
        'sponsors': provider['sponsors'],
    }

    text_and_terms: TextAndTerms = {
        'text': provider['text'],
    }

    result = Sponsors().replace_text_terms(
        game_state,
        text_and_terms,
    )

    assert result == {
        'text': provider['expected_text'],
    }
