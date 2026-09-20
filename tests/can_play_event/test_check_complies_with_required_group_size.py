from dataclasses import replace
from typing import TypedDict

import pytest

from domain.event_rules.groups import Groups
from domain.tribute import Tribute
from domain.types import Event, GroupSizeType
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
    expected_complies_with_required_group_size: bool


providers: list[ProviderType] = [
    (
        {
            'id': 'an event without a required group size can be played',
            'event': default_event,
            'tribute': default_tribute,
            'tributes_remaining': {},
            'expected_complies_with_required_group_size': True,
        }
    ),
    (
        {
            'id': 'an event with a required group size of 1 can be played',
            'event': {
                **default_event,
                'require_group_size': {
                    'type': GroupSizeType.EXACT,
                    'amount': 1,
                },
            },
            'tribute': default_tribute,
            'tributes_remaining': {},
            'expected_complies_with_required_group_size': True,
        }
    ),
    (
        {
            'id': 'an event with a required exact group size of 1 cannot be played if the tribute is grouped with another tribute',
            'event': {
                **default_event,
                'require_group_size': {
                    'type': GroupSizeType.EXACT,
                    'amount': 1,
                },
            },
            'tribute': replace(default_tribute, grouped_with=['Tribute 2']),
            'tributes_remaining': {},
            'expected_complies_with_required_group_size': False,
        }
    ),
    (
        {
            'id': 'an event with a required exact group size of 2 can be played if the tribute is grouped with another tribute',
            'event': {
                **default_event,
                'require_group_size': {
                    'type': GroupSizeType.EXACT,
                    'amount': 2,
                },
            },
            'tribute': replace(default_tribute, grouped_with=['Tribute 2']),
            'tributes_remaining': {},
            'expected_complies_with_required_group_size': True,
        }
    ),
    (
        {
            'id': 'an event with a required minimum group size of 1 can be played if the tribute is not grouped with another tribute',
            'event': {
                **default_event,
                'require_group_size': {'type': GroupSizeType.MIN, 'amount': 1},
            },
            'tribute': default_tribute,
            'tributes_remaining': {},
            'expected_complies_with_required_group_size': True,
        }
    ),
    (
        {
            'id': 'an event with a required minimum group size of 2 can be played if the tribute is grouped with another tribute',
            'event': {
                **default_event,
                'require_group_size': {'type': GroupSizeType.MIN, 'amount': 2},
            },
            'tribute': replace(default_tribute, grouped_with=['Tribute 2']),
            'tributes_remaining': {'Tribute 2': default_tribute},
            'expected_complies_with_required_group_size': True,
        }
    ),
    (
        {
            'id': 'an event with a required minimum group size of 2 cannot be played if the tribute is not grouped with another tribute',
            'event': {
                **default_event,
                'require_group_size': {'type': GroupSizeType.MIN, 'amount': 2},
            },
            'tribute': default_tribute,
            'tributes_remaining': {},
            'expected_complies_with_required_group_size': False,
        }
    ),
    (
        {
            'id': 'an event with a required minimum group size of 2 cannot be played if the tribute is grouped with another tribute but no tributes are remaining',
            'event': {
                **default_event,
                'require_group_size': {'type': GroupSizeType.MIN, 'amount': 2},
            },
            'tribute': replace(default_tribute, grouped_with=['Tribute 2']),
            'tributes_remaining': {},
            'expected_complies_with_required_group_size': False,
        }
    ),
    (
        {
            'id': 'an event with a required minimum group size of 2 cannot be played if the tribute is grouped with another tribute but that tribute is not remaining',
            'event': {
                **default_event,
                'require_group_size': {'type': GroupSizeType.MIN, 'amount': 2},
            },
            'tribute': replace(default_tribute, grouped_with=['Tribute 2']),
            'tributes_remaining': {'Tribute 3': default_tribute},
            'expected_complies_with_required_group_size': False,
        }
    ),
    (
        {
            'id': 'an event with a required maximum group size of 1 can be played if the tribute is not grouped with another tribute',
            'event': {
                **default_event,
                'require_group_size': {'type': GroupSizeType.MAX, 'amount': 1},
            },
            'tribute': default_tribute,
            'tributes_remaining': {},
            'expected_complies_with_required_group_size': True,
        }
    ),
    (
        {
            'id': 'an event with a required maximum group size of 2 can be played if the tribute is not grouped with another tribute',
            'event': {
                **default_event,
                'require_group_size': {'type': GroupSizeType.MAX, 'amount': 2},
            },
            'tribute': default_tribute,
            'tributes_remaining': {},
            'expected_complies_with_required_group_size': True,
        }
    ),
    (
        {
            'id': 'an event with a required maximum group size of 2 can be played if the tribute is grouped with another tribute',
            'event': {
                **default_event,
                'require_group_size': {'type': GroupSizeType.MAX, 'amount': 2},
            },
            'tribute': replace(default_tribute, grouped_with=['Tribute 2']),
            'tributes_remaining': {},
            'expected_complies_with_required_group_size': True,
        }
    ),
    (
        {
            'id': 'an event with a required maximum group size of 1 cannot be played if the tribute is grouped with another tribute',
            'event': {
                **default_event,
                'require_group_size': {'type': GroupSizeType.MAX, 'amount': 1},
            },
            'tribute': replace(default_tribute, grouped_with=['Tribute 2']),
            'tributes_remaining': {},
            'expected_complies_with_required_group_size': False,
        }
    ),
    (
        {
            'id': 'an event with a required maximum group size of 1 cannot be played if the tribute is grouped with another tribute, even if not remaining',
            'event': {
                **default_event,
                'require_group_size': {'type': GroupSizeType.MAX, 'amount': 1},
            },
            'tribute': replace(default_tribute, grouped_with=['Tribute 2']),
            'tributes_remaining': {},
            'expected_complies_with_required_group_size': False,
        }
    ),
]


@pytest.mark.parametrize('provider', providers, ids=lambda p: f'{p["id"]}')
def test_check_complies_with_required_group_size(provider: ProviderType):
    result = Groups().can_play_event(
        provider['event'],
        {
            **default_game_round_state_without_event,
            'current_tribute': provider['tribute'],
            'tributes_remaining_this_round': provider['tributes_remaining'],
        },
    )

    assert result == provider['expected_complies_with_required_group_size']
