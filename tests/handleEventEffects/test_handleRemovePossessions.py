import pytest
import vars
from unittest.mock import call
from handleEventEffects import handleRemovePossessions

@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object( vars, "tributes", {
    "Tribute1": { "name": "Tribute1" },
    "Tribute2": { "name": "Tribute2" },
    "Tribute3": { "name": "Tribute3" },
  } )

def test_handleRemovePossessions(mocker):
  event = { "removePossessions": [
    { "player": 1, "type": "item", "value": "bow" },
    { "player": 3, "type": "pet", "value": "(Animal1)" },
  ] }
  players = [
    { "name": "Tribute1" },
    { "name": "Tribute2" },
    { "name": "Tribute3" },
  ]
  terms = {
    "(Animal1)": "cat"
  }

  removePossessionMock = mocker.patch("handleEventEffects.removePossession")
  
  result = handleRemovePossessions(event, players, terms)

  removePossessionMock.assert_has_calls([
    call({ "name": "Tribute1" }, "item", "bow"),
    call({ "name": "Tribute3" }, "pet", "cat")
  ])
