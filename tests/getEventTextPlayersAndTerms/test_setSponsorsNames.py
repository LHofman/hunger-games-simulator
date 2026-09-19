import pytest

from pytest_mock import MockerFixture
from typing import TypedDict

from Domain.EventRules.Sponsors import Sponsors
from Domain.EventRule import TextAndTerms
from Domain.types import GameRoundState, Tribute
from tests.defaults import (
    defaultGameOptions,
    defaultGameRoundState,
    defaultTribute,
)


class ProviderType(TypedDict):
    id: str
    text: str
    oneSponsorPerTribute: bool
    tribute: Tribute
    sponsors: list[str]
    expectedText: str


@pytest.fixture(autouse=True)
def test_mock(mocker: MockerFixture):
    mocker.patch( 'random.random', return_value=0.5 )
    mocker.patch(
        'random.choice',
        side_effect=lambda list: list[0] # type: ignore
    )


providers: list[ProviderType] = [
    ({
        'id': 'Text without (Sponsor) placeholder doesn\'t change.',
        'text': 'Tribute explores the arena.',
        'oneSponsorPerTribute': True,
        'tribute': { **defaultTribute, 'index': 2 },
        'sponsors': ['Sponsor1', 'Sponsor2'],
        'expectedText': 'Tribute explores the arena.',
    }),
    ({
        'id': 'If the option oneSponsorPerTribute is disabled, a random sponsor is chosen',
        'text': 'Tribute receives a bow, some arrows, and a quiver from (Sponsor).',
        'oneSponsorPerTribute': False,
        'tribute': { **defaultTribute, 'index': 2 },
        'sponsors': ['Sponsor1', 'Sponsor2'],
        'expectedText': 'Tribute receives a bow, some arrows, and a quiver from Sponsor1.',
    }),
    ({
        'id': 'If there are more sponsors than tributes, a random sponsor is chosen',
        'text': 'Tribute receives a bow, some arrows, and a quiver from (Sponsor).',
        'oneSponsorPerTribute': True,
        'tribute': { **defaultTribute, 'index': 2 },
        'sponsors': ['Sponsor1', 'Sponsor2', 'Sponsor3'],
        'expectedText': 'Tribute receives a bow, some arrows, and a quiver from Sponsor1.',
    }),
    ({
        'id': 'If there are less sponsors than tributes, a random sponsor is chosen',
        'text': 'Tribute receives a bow, some arrows, and a quiver from (Sponsor).',
        'oneSponsorPerTribute': True,
        'tribute': { **defaultTribute, 'index': 2 },
        'sponsors': ['Sponsor3'],
        'expectedText': 'Tribute receives a bow, some arrows, and a quiver from Sponsor3.',
    }),
    ({
        'id': 'A tribute receives an item from their respective sponsor',
        'text': 'Tribute receives a bow, some arrows, and a quiver from (Sponsor).',
        'oneSponsorPerTribute': True,
        'tribute': { **defaultTribute, 'index': 2 },
        'sponsors': ['Sponsor1', 'Sponsor2'],
        'expectedText': 'Tribute receives a bow, some arrows, and a quiver from Sponsor2.',
    }),
    ({
        'id': 'A tribute receives an item from an opposing sponsor',
        'text': 'Tribute receives a bow, some arrows, and a quiver from (Sponsor::opposing).',
        'oneSponsorPerTribute': True,
        'tribute': { **defaultTribute, 'index': 2 },
        'sponsors': ['Sponsor1', 'Sponsor2'],
        'expectedText': 'Tribute receives a bow, some arrows, and a quiver from Sponsor1.',
    }),
]


@pytest.mark.parametrize('provider', providers, ids=lambda p: f'{p["id"]}')
def test_setSponsorsNames(provider: ProviderType):
    gameState: GameRoundState = {
        **defaultGameRoundState,
        'totalTributes': 2,
        'options': {
            **defaultGameOptions,
            'oneSponsorPerTribute': provider['oneSponsorPerTribute']
        },
        'currentTribute': provider['tribute'],
        'sponsors': provider['sponsors'],
    }

    textAndTerms: TextAndTerms = {
        'text': provider['text'],
    }

    result = Sponsors().replaceTextTerms(
        gameState,
        textAndTerms
    )

    assert result == {
        'text': provider['expectedText'],
    }
