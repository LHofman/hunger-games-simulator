import pytest
import random
from getEventTextPlayersAndTerms import setPlayersNames

@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch(
    "random.choice",
    side_effect=lambda list: list[0]
  )

def test_setPlayersNames():
  event = { "text": "(Player1) is working with (Player2) to kill (Player3)" }
  tribute = { "name": "Tribute", "groupedWith": ["Friend 1", "Friend 2"] }
  playersRemaining = { "Friend 2": { "name": "Friend 2" }, "Enemy": { "name": "Enemy" } }
  aoGroupPlayersRequired = 2
  groupedWithPlayers = { "Friend 2": { "name": "Friend 2" } }

  result = setPlayersNames(
    event,
    tribute,
    playersRemaining,
    aoGroupPlayersRequired,
    groupedWithPlayers
  )

  assert result == (
    [
      { "name": "Tribute", "groupedWith": ["Friend 1", "Friend 2"] },
      { "name": "Friend 2" },
      { "name": "Enemy" }
    ],
    "Tribute is working with Friend 2 to kill Enemy"
  )
