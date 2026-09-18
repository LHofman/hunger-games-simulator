import pytest
from canPlayEvent import checkCompliesWithRequiredGroupSize

providers = [
  ({
    "id": "an event without a required group size can be played",
    "event": {},
    "tribute": {},
    "playersRemaining": {},
    "expectedCompliesWithRequiredGroupSize": True,
  }),
  ({
    "id": "an event with a required group size of 1 can be played",
    "event": { "requireGroupSize": { "type": "exact", "amount": 1 } },
    "tribute": { "groupedWith": [] },
    "playersRemaining": {},
    "expectedCompliesWithRequiredGroupSize": True,
  }),
  ({
    "id": "an event with a required exact group size of 1 cannot be played if the tribute is grouped with another player",
    "event": { "requireGroupSize": { "type": "exact", "amount": 1 } },
    "tribute": { "groupedWith": [ "Player 2" ] },
    "playersRemaining": {},
    "expectedCompliesWithRequiredGroupSize": False,
  }),
  ({
    "id": "an event with a required exact group size of 2 can be played if the tribute is grouped with another player",
    "event": { "requireGroupSize": { "type": "exact", "amount": 2 } },
    "tribute": { "groupedWith": [ "Player 2" ] },
    "playersRemaining": {},
    "expectedCompliesWithRequiredGroupSize": True,
  }),
  ({
    "id": "an event with a required minimum group size of 1 can be played if the tribute is not grouped with another player",
    "event": { "requireGroupSize": { "type": "min", "amount": 1 } },
    "tribute": { "groupedWith": [] },
    "playersRemaining": {},
    "expectedCompliesWithRequiredGroupSize": True,
  }),
  ({
    "id": "an event with a required minimum group size of 2 can be played if the tribute is grouped with another player",
    "event": { "requireGroupSize": { "type": "min", "amount": 2 } },
    "tribute": { "groupedWith": [ "Player 2" ] },
    "playersRemaining": { "Player 2": {} },
    "expectedCompliesWithRequiredGroupSize": True,
  }),
  ({
    "id": "an event with a required minimum group size of 2 cannot be played if the tribute is not grouped with another player",
    "event": { "requireGroupSize": { "type": "min", "amount": 2 } },
    "tribute": { "groupedWith": [] },
    "playersRemaining": {},
    "expectedCompliesWithRequiredGroupSize": False,
  }),
  ({
    "id": "an event with a required minimum group size of 2 cannot be played if the tribute is grouped with another player but no players are remaining",
    "event": { "requireGroupSize": { "type": "min", "amount": 2 } },
    "tribute": { "groupedWith": [ "Player 2" ] },
    "playersRemaining": {},
    "expectedCompliesWithRequiredGroupSize": False,
  }),
  ({
    "id": "an event with a required minimum group size of 2 cannot be played if the tribute is grouped with another player but that player is not remaining",
    "event": { "requireGroupSize": { "type": "min", "amount": 2 } },
    "tribute": { "groupedWith": [ "Player 2" ] },
    "playersRemaining": { "Player 3": {} },
    "expectedCompliesWithRequiredGroupSize": False,
  }),
  ({
    "id": "an event with a required maximum group size of 1 can be played if the tribute is not grouped with another player",
    "event": { "requireGroupSize": { "type": "max", "amount": 1 } },
    "tribute": { "groupedWith": [] },
    "playersRemaining": {},
    "expectedCompliesWithRequiredGroupSize": True,
  }),
  ({
    "id": "an event with a required maximum group size of 2 can be played if the tribute is not grouped with another player",
    "event": { "requireGroupSize": { "type": "max", "amount": 2 } },
    "tribute": { "groupedWith": [] },
    "playersRemaining": {},
    "expectedCompliesWithRequiredGroupSize": True,
  }),
  ({
    "id": "an event with a required maximum group size of 2 can be played if the tribute is grouped with another player",
    "event": { "requireGroupSize": { "type": "max", "amount": 2 } },
    "tribute": { "groupedWith": [ "Player 2" ] },
    "playersRemaining": {},
    "expectedCompliesWithRequiredGroupSize": True,
  }),
  ({
    "id": "an event with a required maximum group size of 1 cannot be played if the tribute is grouped with another player",
    "event": { "requireGroupSize": { "type": "max", "amount": 1 } },
    "tribute": { "groupedWith": [ "Player 2" ] },
    "playersRemaining": {},
    "expectedCompliesWithRequiredGroupSize": False,
  }),
  ({
    "id": "an event with a required maximum group size of 1 cannot be played if the tribute is grouped with another player, even if not remaining",
    "event": { "requireGroupSize": { "type": "max", "amount": 1 } },
    "tribute": { "groupedWith": [ "Player 2" ] },
    "playersRemaining": {},
    "expectedCompliesWithRequiredGroupSize": False,
  }),
]

@pytest.mark.parametrize("provider", providers, ids=lambda p: f"{p['id']}")
def test_checkCompliesWithRequiredGroupSize(provider):
  result = checkCompliesWithRequiredGroupSize(
    provider["tribute"],
    provider["event"],
    provider["playersRemaining"]
  )
  assert result == provider["expectedCompliesWithRequiredGroupSize"]
