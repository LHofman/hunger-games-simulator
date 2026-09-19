from typing import TypedDict
import pytest

from Domain.EventRules.Groups import Groups
from Domain.types import Event, GroupSizeType, Tribute
from tests.defaults import (
  defaultEvent,
  defaultGameRoundStateWithoutEvent,
  defaultTribute,
)

class ProviderType(TypedDict):
  id: str
  event: Event
  tribute: Tribute
  playersRemaining: dict[str, Tribute]
  expectedCompliesWithRequiredGroupSize: bool

providers: list[ProviderType] = [
  ({
    'id': 'an event without a required group size can be played',
    'event': defaultEvent,
    'tribute': defaultTribute,
    'playersRemaining': {},
    'expectedCompliesWithRequiredGroupSize': True,
  }),
  ({
    'id': 'an event with a required group size of 1 can be played',
    'event': { **defaultEvent, 'requireGroupSize': { 'type': GroupSizeType.EXACT, 'amount': 1 } },
    'tribute': { **defaultTribute, 'groupedWith': [] },
    'playersRemaining': {},
    'expectedCompliesWithRequiredGroupSize': True,
  }),
  ({
    'id': 'an event with a required exact group size of 1 cannot be played if the tribute is grouped with another player',
    'event': { **defaultEvent, 'requireGroupSize': { 'type': GroupSizeType.EXACT, 'amount': 1 } },
    'tribute': { **defaultTribute, 'groupedWith': [ 'Player 2' ] },
    'playersRemaining': {},
    'expectedCompliesWithRequiredGroupSize': False,
  }),
  ({
    'id': 'an event with a required exact group size of 2 can be played if the tribute is grouped with another player',
    'event': { **defaultEvent, 'requireGroupSize': { 'type': GroupSizeType.EXACT, 'amount': 2 } },
    'tribute': { **defaultTribute, 'groupedWith': [ 'Player 2' ] },
    'playersRemaining': {},
    'expectedCompliesWithRequiredGroupSize': True,
  }),
  ({
    'id': 'an event with a required minimum group size of 1 can be played if the tribute is not grouped with another player',
    'event': { **defaultEvent, 'requireGroupSize': { 'type': GroupSizeType.MIN, 'amount': 1 } },
    'tribute': { **defaultTribute, 'groupedWith': [] },
    'playersRemaining': {},
    'expectedCompliesWithRequiredGroupSize': True,
  }),
  ({
    'id': 'an event with a required minimum group size of 2 can be played if the tribute is grouped with another player',
    'event': { **defaultEvent, 'requireGroupSize': { 'type': GroupSizeType.MIN, 'amount': 2 } },
    'tribute': { **defaultTribute, 'groupedWith': [ 'Player 2' ] },
    'playersRemaining': { 'Player 2': defaultTribute },
    'expectedCompliesWithRequiredGroupSize': True,
  }),
  ({
    'id': 'an event with a required minimum group size of 2 cannot be played if the tribute is not grouped with another player',
    'event': { **defaultEvent, 'requireGroupSize': { 'type': GroupSizeType.MIN, 'amount': 2 } },
    'tribute': { **defaultTribute, 'groupedWith': [] },
    'playersRemaining': {},
    'expectedCompliesWithRequiredGroupSize': False,
  }),
  ({
    'id': 'an event with a required minimum group size of 2 cannot be played if the tribute is grouped with another player but no players are remaining',
    'event': { **defaultEvent, 'requireGroupSize': { 'type': GroupSizeType.MIN, 'amount': 2 } },
    'tribute': { **defaultTribute, 'groupedWith': [ 'Player 2' ] },
    'playersRemaining': {},
    'expectedCompliesWithRequiredGroupSize': False,
  }),
  ({
    'id': 'an event with a required minimum group size of 2 cannot be played if the tribute is grouped with another player but that player is not remaining',
    'event': { **defaultEvent, 'requireGroupSize': { 'type': GroupSizeType.MIN, 'amount': 2 } },
    'tribute': { **defaultTribute, 'groupedWith': [ 'Player 2' ] },
    'playersRemaining': { 'Player 3': defaultTribute },
    'expectedCompliesWithRequiredGroupSize': False,
  }),
  ({
    'id': 'an event with a required maximum group size of 1 can be played if the tribute is not grouped with another player',
    'event': { **defaultEvent, 'requireGroupSize': { 'type': GroupSizeType.MAX, 'amount': 1 } },
    'tribute': { **defaultTribute, 'groupedWith': [] },
    'playersRemaining': {},
    'expectedCompliesWithRequiredGroupSize': True,
  }),
  ({
    'id': 'an event with a required maximum group size of 2 can be played if the tribute is not grouped with another player',
    'event': { **defaultEvent, 'requireGroupSize': { 'type': GroupSizeType.MAX, 'amount': 2 } },
    'tribute': { **defaultTribute, 'groupedWith': [] },
    'playersRemaining': {},
    'expectedCompliesWithRequiredGroupSize': True,
  }),
  ({
    'id': 'an event with a required maximum group size of 2 can be played if the tribute is grouped with another player',
    'event': { **defaultEvent, 'requireGroupSize': { 'type': GroupSizeType.MAX, 'amount': 2 } },
    'tribute': { **defaultTribute, 'groupedWith': [ 'Player 2' ] },
    'playersRemaining': {},
    'expectedCompliesWithRequiredGroupSize': True,
  }),
  ({
    'id': 'an event with a required maximum group size of 1 cannot be played if the tribute is grouped with another player',
    'event': { **defaultEvent, 'requireGroupSize': { 'type': GroupSizeType.MAX, 'amount': 1 } },
    'tribute': { **defaultTribute, 'groupedWith': [ 'Player 2' ] },
    'playersRemaining': {},
    'expectedCompliesWithRequiredGroupSize': False,
  }),
  ({
    'id': 'an event with a required maximum group size of 1 cannot be played if the tribute is grouped with another player, even if not remaining',
    'event': { **defaultEvent, 'requireGroupSize': { 'type': GroupSizeType.MAX, 'amount': 1 } },
    'tribute': { **defaultTribute, 'groupedWith': [ 'Player 2' ] },
    'playersRemaining': {},
    'expectedCompliesWithRequiredGroupSize': False,
  }),
]

@pytest.mark.parametrize('provider', providers, ids=lambda p: f'{p["id"]}')
def test_checkCompliesWithRequiredGroupSize(provider: ProviderType):
  result = Groups().canPlayEvent(
    provider['event'],
    {
      **defaultGameRoundStateWithoutEvent,
      'currentTribute': provider['tribute'],
      'playersRemainingThisRound': provider['playersRemaining']
    }
  )

  assert result == provider['expectedCompliesWithRequiredGroupSize']
