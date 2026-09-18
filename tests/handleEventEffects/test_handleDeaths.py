import pytest
import vars
from unittest.mock import call
from handleEventEffects import handleDeaths

@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object( vars, "tributes", {
    "Tribute1": { "name": "Tribute1", "groupedWith": ["Tribute2", "Tribute3"] },
    "Tribute2": { "name": "Tribute2", "groupedWith": [] },
    "Tribute3": { "name": "Tribute3", "groupedWith": [] },
  } )

def test_handleDeaths(mocker):
  event = { "deaths": ["Player2", "Player3"] }
  players = [
    { "name": "Tribute1", "district": 1 },
    { "name": "Tribute2", "district": 2 },
    { "name": "Tribute3", "district": 3 },
  ]
  exactTime = "day"

  updateTributesDataMock = mocker.patch("handleEventEffects.updateTributesData")
  
  result = handleDeaths(event, players, exactTime)

  assert vars.recentDeaths == [("Tribute2", 2), ("Tribute3", 3)]
  updateTributesDataMock.assert_has_calls([
    call({ "name": "Tribute2", "district": 2 }, "time of death", "", "day"),
    call({ "name": "Tribute2", "district": 2 }, "district", "", 2),
    call({ "name": "Tribute3", "district": 3 }, "time of death", "", "day"),
    call({ "name": "Tribute3", "district": 3 }, "district", "", 3),
  ])
  assert vars.tributes == {
    "Tribute1": { "name": "Tribute1", "groupedWith": [] },
  }
