import pytest
import vars
from getEvent import getIncreasedOddsEventsFromGameSpeed

# Mock tribute possessions, alsways has "Test Item 1" and "Test Item 2"
@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object( vars, "gameData", { "options": { "speed": 10 }, }, )
  mocker.patch.object(
    vars,
    "events",
    {
      "findAnimalButItRunsAway": {
        "text": "(Player1) finds a (Animal1), it runs away scared"
      },
      "dieFromHypothermia": {
        "text": "(Player1) dies from hypothermia.",
        "requiresPossessions": [{ "player": 1, "type": "status", "value": "cold" }],
        "percentage": 250,
        "deaths": ["Player1"]
      },
      "killOnePlayer1": {
        "text": "(Player2) catches (Player1) off guard and kills them.",
        "players": 2,
        "deaths": ["Player1"],
        "updateTributesData": [{ "player": 1, "type": "kills", "operation": "add", "value": 1 }]
      },
    },
  )

providers = [
  ({ "id": "speed 1 should have lower death percentage", "speed": 1, "percentage": -80, }),
  ({ "id": "speed 2 should have lower death percentage", "speed": 2, "percentage": -60, }),
  ({ "id": "speed 3 should have lower death percentage", "speed": 3, "percentage": -40, }),
  ({ "id": "speed 4 should have lower death percentage", "speed": 4, "percentage": -20, }),
  ({ "id": "speed 6 should have higher death percentage", "speed": 6, "percentage": 20, }),
  ({ "id": "speed 7 should have higher death percentage", "speed": 7, "percentage": 40, }),
  ({ "id": "speed 8 should have higher death percentage", "speed": 8, "percentage": 60, }),
  ({ "id": "speed 9 should have higher death percentage", "speed": 9, "percentage": 80, }),
  ({ "id": "speed 10 should have higher death percentage", "speed": 10, "percentage": 100, }),
]

@pytest.mark.parametrize("provider", providers, ids=lambda p: f"{p['id']}")
def test_getIncreasedOddsEventsFromGameSpeed(provider, mocker):
  mocker.patch.object( vars, "gameData", { "options": { "speed": provider["speed"] }, }, )

  result = getIncreasedOddsEventsFromGameSpeed()

  assert result == [
    { "event": "dieFromHypothermia", "percentage": provider["percentage"] },
    { "event": "killOnePlayer1", "percentage": provider["percentage"] },
  ]
