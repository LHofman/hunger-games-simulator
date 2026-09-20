from typing import TypedDict

import pytest

from domain.event_rules.possessions import Possessions
from domain.types import Event, GameRoundStateWithoutEvent
from tests.defaults import (
    default_event,
    default_game_round_state_without_event,
    default_tribute,
)


class ProviderType(TypedDict):
    id: str
    event: Event
    expected_has_required_possessions: bool


providers: list[ProviderType] = [
    (
        {
            'id': 'an event without required possessions can be played',
            'event': {**default_event, 'name': 'Test Event'},
            'expected_has_required_possessions': True,
        }
    ),
    (
        {
            'id': 'an event with a required possession that the tribute has can be played',
            'event': {
                **default_event,
                'name': 'Test Event',
                'requires_possessions': [
                    {'tribute': 1, 'type': 'item', 'value': 'Test Item 1'}
                ],
            },
            'expected_has_required_possessions': True,
        }
    ),
    (
        {
            'id': 'an event with a required possession that the tribute does not have cannot be played',
            'event': {
                **default_event,
                'name': 'Test Event',
                'requires_possessions': [
                    {'tribute': 1, 'type': 'item', 'value': 'Test Item 3'}
                ],
            },
            'expected_has_required_possessions': False,
        }
    ),
    (
        {
            'id': 'an event with a required possession that the tribute does not have but is negated can be played',
            'event': {
                **default_event,
                'name': 'Test Event',
                'requires_possessions': [
                    {
                        'tribute': 1,
                        'type': 'item',
                        'value': 'Test Item 3',
                        'inverse': True,
                    }
                ],
            },
            'expected_has_required_possessions': True,
        }
    ),
    (
        {
            'id': 'an event with a required possession that the tribute has but is negated cannot be played',
            'event': {
                **default_event,
                'name': 'Test Event',
                'requires_possessions': [
                    {
                        'tribute': 1,
                        'type': 'item',
                        'value': 'Test Item 1',
                        'inverse': True,
                    }
                ],
            },
            'expected_has_required_possessions': False,
        }
    ),
    (
        {
            'id': 'an event with multiple required possessions that the tribute has can be played',
            'event': {
                **default_event,
                'name': 'Test Event',
                'requires_possessions': [
                    {'tribute': 1, 'type': 'item', 'value': 'Test Item 1'},
                    {'tribute': 1, 'type': 'item', 'value': 'Test Item 2'},
                ],
            },
            'expected_has_required_possessions': True,
        }
    ),
    (
        {
            'id': 'an event with multiple required possessions that the tribute does not have cannot be played',
            'event': {
                **default_event,
                'name': 'Test Event',
                'requires_possessions': [
                    {'tribute': 1, 'type': 'item', 'value': 'Test Item 1'},
                    {'tribute': 1, 'type': 'item', 'value': 'Test Item 3'},
                ],
            },
            'expected_has_required_possessions': False,
        }
    ),
    (
        {
            'id': 'an event with multiple required possessions that the tribute has and does not have but is negated can be played',
            'event': {
                **default_event,
                'name': 'Test Event',
                'requires_possessions': [
                    {'tribute': 1, 'type': 'item', 'value': 'Test Item 1'},
                    {
                        'tribute': 1,
                        'type': 'item',
                        'value': 'Test Item 3',
                        'inverse': True,
                    },
                ],
            },
            'expected_has_required_possessions': True,
        }
    ),
    (
        {
            'id': 'an event with multiple required possessions that the tribute has and does have but is negated cannot be played',
            'event': {
                **default_event,
                'name': 'Test Event',
                'requires_possessions': [
                    {'tribute': 1, 'type': 'item', 'value': 'Test Item 1'},
                    {
                        'tribute': 1,
                        'type': 'item',
                        'value': 'Test Item 2',
                        'inverse': True,
                    },
                ],
            },
            'expected_has_required_possessions': False,
        }
    ),
    (
        {
            'id': 'an event with multiple required possessions that the tribute does not have and does have but is negated cannot be played',
            'event': {
                **default_event,
                'name': 'Test Event',
                'requires_possessions': [
                    {'tribute': 1, 'type': 'item', 'value': 'Test Item 3'},
                    {
                        'tribute': 1,
                        'type': 'item',
                        'value': 'Test Item 4',
                        'inverse': True,
                    },
                ],
            },
            'expected_has_required_possessions': False,
        }
    ),
]


@pytest.mark.parametrize('provider', providers, ids=lambda p: f'{p["id"]}')
def test_check_has_required_possessions(provider: ProviderType):
    game_state: GameRoundStateWithoutEvent = {
        **default_game_round_state_without_event,
        'current_tribute': {
            **default_tribute,
            'possessions': {
                'item': ['Test Item 1', 'Test Item 2'],
            },
        },
    }
    result = Possessions().can_play_event(
        provider['event'],
        game_state,
    )

    assert result == provider['expected_has_required_possessions']
