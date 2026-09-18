import pytest
import vars
from handleEventEffects import handleFormGroup

@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object( vars, "tributes", {
    "Tribute1": { "name": "Tribute1", "groupedWith": [] },
    "Tribute2": { "name": "Tribute2", "groupedWith": [] },
    "Tribute3": { "name": "Tribute3", "groupedWith": [] },
  } )

def test_handleFormGroup():
  event = { "formGroup": ["Player1", "Player2"] }
  players = [
    { "name": "Tribute1" },
    { "name": "Tribute2" },
  ]

  result = handleFormGroup(event, players)

  assert vars.tributes["Tribute1"]["groupedWith"] == ["Tribute2"]
  assert vars.tributes["Tribute2"]["groupedWith"] == ["Tribute1"]
