from typing import TypedDict
import pytest
from Domain.EventRules.Possessions import Possessions
from Domain.types import Event, GameRoundStateWithoutEvent
from tests.defaults import (
  defaultEvent,
  defaultGameRoundStateWithoutEvent,
  defaultTribute
)

class ProviderType(TypedDict):
  id: str
  event: Event
  expectedHasRequiredPossessions: bool

providers: list[ProviderType] = [
  ({
    'id': 'an event without required possessions can be played',
    'event': { **defaultEvent, 'name': 'Test Event' },
    'expectedHasRequiredPossessions': True,
  }),
  ({
    'id': 'an event with a required possession that the tribute has can be played',
    'event': { **defaultEvent, 'name': 'Test Event', 'requiresPossessions': [{ 'player': 1, 'type': 'item', 'value': 'Test Item 1' }] },
    'expectedHasRequiredPossessions': True,
  }),
  ({
    'id': 'an event with a required possession that the tribute does not have cannot be played',
    'event': { **defaultEvent, 'name': 'Test Event', 'requiresPossessions': [{ 'player': 1, 'type': 'item', 'value': 'Test Item 3' }] },
    'expectedHasRequiredPossessions': False,
  }),
  ({
    'id': 'an event with a required possession that the tribute does not have but is negated can be played',
    'event': { **defaultEvent, 'name': 'Test Event', 'requiresPossessions': [{ 'player': 1, 'type': 'item', 'value': 'Test Item 3', 'inverse': True }] },
    'expectedHasRequiredPossessions': True,
  }),
  ({
    'id': 'an event with a required possession that the tribute has but is negated cannot be played',
    'event': { **defaultEvent, 'name': 'Test Event', 'requiresPossessions': [{ 'player': 1, 'type': 'item', 'value': 'Test Item 1', 'inverse': True }] },
    'expectedHasRequiredPossessions': False,
  }),
  ({
    'id': 'an event with multiple required possessions that the tribute has can be played',
    'event': { **defaultEvent, 'name': 'Test Event', 'requiresPossessions': [{ 'player': 1, 'type': 'item', 'value': 'Test Item 1' }, { 'player': 1, 'type': 'item', 'value': 'Test Item 2' }] },
    'expectedHasRequiredPossessions': True,
  }),
  ({
    'id': 'an event with multiple required possessions that the tribute does not have cannot be played',
    'event': { **defaultEvent, 'name': 'Test Event', 'requiresPossessions': [{ 'player': 1, 'type': 'item', 'value': 'Test Item 1' }, { 'player': 1, 'type': 'item', 'value': 'Test Item 3' }] },
    'expectedHasRequiredPossessions': False,
  }),
  ({
    'id': 'an event with multiple required possessions that the tribute has and does not have but is negated can be played',
    'event': { **defaultEvent, 'name': 'Test Event', 'requiresPossessions': [{ 'player': 1, 'type': 'item', 'value': 'Test Item 1' }, { 'player': 1, 'type': 'item', 'value': 'Test Item 3', 'inverse': True }] },
    'expectedHasRequiredPossessions': True,
  }),
  ({
    'id': 'an event with multiple required possessions that the tribute has and does have but is negated cannot be played',
    'event': { **defaultEvent, 'name': 'Test Event', 'requiresPossessions': [{ 'player': 1, 'type': 'item', 'value': 'Test Item 1' }, { 'player': 1, 'type': 'item', 'value': 'Test Item 2', 'inverse': True }] },
    'expectedHasRequiredPossessions': False,
  }),
  ({
    'id': 'an event with multiple required possessions that the tribute does not have and does have but is negated cannot be played',
    'event': { **defaultEvent, 'name': 'Test Event', 'requiresPossessions': [{ 'player': 1, 'type': 'item', 'value': 'Test Item 3' }, { 'player': 1, 'type': 'item', 'value': 'Test Item 4', 'inverse': True }] },
    'expectedHasRequiredPossessions': False,
  })
]

@pytest.mark.parametrize('provider', providers, ids=lambda p: f'{p["id"]}')
def test_checkHasRequiredPossessions(provider: ProviderType):
  gameState: GameRoundStateWithoutEvent = {
    **defaultGameRoundStateWithoutEvent,
    'currentTribute': {
      **defaultTribute,
      'possessions': {
        'item': ['Test Item 1', 'Test Item 2'],
      }
    }
  }
  result = Possessions().canPlayEvent(
    provider['event'],
    gameState
  )

  assert result == provider['expectedHasRequiredPossessions']
