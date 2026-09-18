import pytest
import vars
from unittest.mock import call
from handleEventEffects import handleAddPossessions

@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object( vars, "tributes", {
    "Tribute1": { "name": "Tribute1" },
    "Tribute2": { "name": "Tribute2" },
    "Tribute3": { "name": "Tribute3" },
  } )

def test_handleAddPossessions(mocker):
  event = { "addPossessions": [
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

  addPossessionMock = mocker.patch("handleEventEffects.addPossession")
  
  result = handleAddPossessions( event, players, terms )

  addPossessionMock.assert_has_calls([
    call({ "name": "Tribute1" }, "item", "bow"),
    call({ "name": "Tribute3" }, "pet", "cat")
  ])
