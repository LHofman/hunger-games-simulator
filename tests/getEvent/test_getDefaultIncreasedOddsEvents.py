import pytest
import vars
from getEvent import getDefaultIncreasedOddsEvents

# Mock tribute possessions, alsways has "Test Item 1" and "Test Item 2"
@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object(
    vars,
    "events",
    {
      "findAnimal": {
        "text": "(Player1) finds a (Animal1)",
        "maxOccurances": 3,
      },
      "findAnimals": {
        "text": "(Player1) finds (Animal1)s",
        "maxOccurances": 3,
      },
      "findAnimalButItRunsAway": {
        "text": "(Player1) finds a (Animal1), it runs away scared",
        "maxOccurances": 3,
      },
      "dieFromHypothermia": {
        "text": "(Player1) dies from hypothermia.",
        "requiresPossessions": [{ "player": 1, "type": "status", "value": "cold" }],
        "percentage": 250,
        "deaths": ["Player1"]
      },
    },
  )
  mocker.patch.object(
    vars,
    "eventsOccured",
    {
      "findAnimals": 2,
      "findAnimalButItRunsAway": 3,
    },
  )

def test_getDefaultIncreasedOddsEvents():
  result = getDefaultIncreasedOddsEvents()

  assert result == [
    { "event": "findAnimalButItRunsAway", "percentage": -100 },
    { "event": "dieFromHypothermia", "percentage": 250 },
  ]
