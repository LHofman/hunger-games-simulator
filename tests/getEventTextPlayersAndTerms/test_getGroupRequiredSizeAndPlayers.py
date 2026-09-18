import pytest
from getEventTextPlayersAndTerms import getGroupRequiredSizeAndPlayers

providers = [
  ({
    "id": "an event without requireGroupSize should not return any players",
    "event": { "name": "Event without requireGroupSize" },
    "tribute": { "groupedWith": ["Player2", "Player3"] },
    "playersRemaining": { "Player3": { "name": "Player3" } },
    "expectedGroupRequiredSizeAndPlayers": (0, {})
  }),
  ({
    "id": "it should only return the players in the tribue's group that are still remaining",
    "event": { "requireGroupSize": { "amount": 2 } },
    "tribute": { "groupedWith": ["Player2", "Player3"] },
    "playersRemaining": { "Player3": { "name": "Player3" } },
    "expectedGroupRequiredSizeAndPlayers": (2, { "Player3": { "name": "Player3" } })
  }),
  ({
    "id": "it should return the correct group size and players when there are multiple players remaining",
    "event": { "requireGroupSize": { "amount": 2 } },
    "tribute": { "groupedWith": ["Player2", "Player3"] },
    "playersRemaining": { "Player2": { "name": "Player2" }, "Player3": { "name": "Player3" } },
    "expectedGroupRequiredSizeAndPlayers": (2, { "Player2": { "name": "Player2" }, "Player3": { "name": "Player3" } })
  }),
]

@pytest.mark.parametrize("provider", providers, ids=lambda p: f"{p['id']}")
def test_getGroupRequiredSizeAndPlayers(provider):
  result = getGroupRequiredSizeAndPlayers(
    provider["event"],
    provider["tribute"],
    provider["playersRemaining"]
  )

  assert result == provider["expectedGroupRequiredSizeAndPlayers"]
