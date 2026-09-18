import pytest
import vars
from handleEventEffects import handleSplitGroup

@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object( vars, "tributes", {
    "Tribute1": { "name": "Tribute1", "groupedWith": ["Tribute2"] },
    "Tribute2": { "name": "Tribute2", "groupedWith": ["Tribute1"] },
    "Tribute3": { "name": "Tribute3", "groupedWith": [] },
  } )

def test_handleSplitGroup():
  event = { "splitGroup": ["Player1", "Player2"] }
  players = [
    { "name": "Tribute1" },
    { "name": "Tribute2" },
  ]

  result = handleSplitGroup(event, players)

  assert vars.tributes["Tribute1"]["groupedWith"] == []
  assert vars.tributes["Tribute2"]["groupedWith"] == []
