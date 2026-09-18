import pytest
import vars
from getEvent import getIncreasedOddsEventsFromPossessions

# Mock tribute possessions, alsways has "Test Item 1" and "Test Item 2"
@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object(
    vars,
    "gameData",
    { "increaseEventOdds": { "possessions": {
      "item": {
        "map": [{ "event": "getLost", "percentage": -95 }]
      },
      "status": {
        "beggedSponsor": [
          { "event": "receiveBow", "percentage": 100 },
        ],
        "cold": [
          { "event": "snuggle", "percentage": 200 },
          { "event": "snuggleAndCaught", "percentage": 200 },
        ],
        "hidden": [
          { "event": "startFire", "percentage": -80 },
        ]
      }
    } } }
  )

def test_getIncreasedOddsEventsFromPossessions():
  tribute = {
    "possessions": {
      "item": ["map"],
      "status": ["beggedSponsor", "cold"],
      "other": ["somethingElse"]
    }
  }

  result = getIncreasedOddsEventsFromPossessions(tribute)

  assert result == [
    { "event": "getLost", "percentage": -95 },
    { "event": "receiveBow", "percentage": 100 },
    { "event": "snuggle", "percentage": 200 },
    { "event": "snuggleAndCaught", "percentage": 200 },
  ]
