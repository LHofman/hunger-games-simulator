import pytest
import vars
from unittest.mock import call
from handleEventEffects import handleAddData

@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object( vars, "tributes", {
    "Tribute1": { "name": "Tribute1" },
    "Tribute2": { "name": "Tribute2" },
    "Tribute3": { "name": "Tribute3" },
  } )

def test_handleAddData(mocker):
  event = { "updateTributesData": [
    { "player": 1, "type": "kills", "operation": "add", "value": 1 },
    { "player": 3, "type": "other", "value": 2 },
  ] }
  players = [
    { "name": "Tribute1" },
    { "name": "Tribute2" },
    { "name": "Tribute3" },
  ]

  updateTributesDataMock = mocker.patch("handleEventEffects.updateTributesData")
  
  result = handleAddData(event, players)

  updateTributesDataMock.assert_has_calls([
    call({ "name": "Tribute1" }, "kills", "add", 1),
    call({ "name": "Tribute3" }, "other", "", 2),
  ])
