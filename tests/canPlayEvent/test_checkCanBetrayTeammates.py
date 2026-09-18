import pytest
import vars
from canPlayEvent import checkCanBetrayTeammates

@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object(
    vars,
    "gameData",
    { "options": { "betrayTeammates": False } }
  )

providers = [
  ({
    "id": "An event without deaths can be played",
    "event": { "name": "Event without deaths" },
    "tribute": { },
    "expectedCanBetrayTeammates": True,
  }),
  ({
    "id": "An event with deaths but no killTeammates can be played",
    "event": { "deaths": ["Player2"] },
    "tribute": { },
    "expectedCanBetrayTeammates": True,
  }),
  ({
    "id": "An event with deaths and killTeammates set to false can be played",
    "event": { "deaths": ["Player2"], "killTeammates": False },
    "tribute": { },
    "expectedCanBetrayTeammates": True,
  }),
  ({
    "id": "An event killTeammates can be played if the tribute is not grouped with any other tributes",
    "event": { "deaths": ["Player2"], "killTeammates": True },
    "tribute": { "groupedWith": [] },
    "expectedCanBetrayTeammates": True,
  }),
  ({
    "id": "An event killTeammates can be played if the tribute is not grouped with the tribute that is killed",
    "event": { "deaths": ["Player2"], "killTeammates": True },
    "tribute": { "groupedWith": ["Player3"] },
    "expectedCanBetrayTeammates": True,
  }),
  ({
    "id": "An event killTeammates cannot be played if the tribute is grouped with the tribute that is killed",
    "event": { "deaths": ["Player2"], "killTeammates": True },
    "tribute": { "groupedWith": ["Player2"] },
    "expectedCanBetrayTeammates": False,
  }),
]

@pytest.mark.parametrize("provider", providers, ids=lambda p: f"{p['id']}")
def test_checkCanBetrayTeammates(provider):
  result = checkCanBetrayTeammates(
    provider["tribute"],
    provider["event"]
  )

  assert result == provider["expectedCanBetrayTeammates"]

def test_canBetrayTeammatesIfOverriddenByOption():
  vars.gameData["options"]["betrayTeammates"] = True
  tribute = { "groupedWith": ["Player1", "Player2"] }
  event = { "deaths": ["Player1"], "killTeammates": True }
  result = checkCanBetrayTeammates(tribute, event)
  assert result == True
