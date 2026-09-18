import pytest
import vars
from unittest.mock import call
from playGame import checkEveryoneInTheSameGroup

providers = [
  ({
    "id": "Game with 2 tributes in same group split up",
    "tributes": {
      "Tribute1": { "name": "Tribute1", "groupedWith": ["Tribute2"] },
      "Tribute2": { "name": "Tribute2", "groupedWith": ["Tribute1"] }
    },
    "expectedEveryoneInTheSameGroup": True,
  }),
  ({
    "id": "Game with 3 tributes in same group split up",
    "tributes": {
      "Tribute1": { "name": "Tribute1", "groupedWith": ["Tribute2", "Tribute3"] },
      "Tribute2": { "name": "Tribute2", "groupedWith": ["Tribute1", "Tribute3"] },
      "Tribute3": { "name": "Tribute3", "groupedWith": ["Tribute1", "Tribute2"] }
    },
    "expectedEveryoneInTheSameGroup": True,
  }),
  ({
    "id": "Game with 2 tributes not in same group don't split up",
    "tributes": {
      "Tribute1": { "name": "Tribute1", "groupedWith": [] },
      "Tribute2": { "name": "Tribute2", "groupedWith": [] }
    },
    "expectedEveryoneInTheSameGroup": False,
  }),
  ({
    "id": "Game with 3 tributes some in same group don't split up",
    "tributes": {
      "Tribute1": { "name": "Tribute1", "groupedWith": ["Tribute2"] },
      "Tribute2": { "name": "Tribute2", "groupedWith": ["Tribute1"] },
      "Tribute3": { "name": "Tribute3", "groupedWith": [] }
    },
    "expectedEveryoneInTheSameGroup": False,
  }),
  ({
    "id": "Game with 4 tributes in two groups don't split up",
    "tributes": {
      "Tribute1": { "name": "Tribute1", "groupedWith": ["Tribute2"] },
      "Tribute2": { "name": "Tribute2", "groupedWith": ["Tribute1"] },
      "Tribute3": { "name": "Tribute3", "groupedWith": ["Tribute4"] },
      "Tribute4": { "name": "Tribute4", "groupedWith": ["Tribute3"] }
    },
    "expectedEveryoneInTheSameGroup": False,
  }),
]

@pytest.mark.parametrize("provider", providers, ids=lambda p: f"{p['id']}")
def test_checkEveryoneInTheSameGroup(provider, mocker):
  mocker.patch.object( vars, "tributes", provider["tributes"] )

  printOutputMock = mocker.patch("playGame.printOutput")
  
  result = checkEveryoneInTheSameGroup()

  if (provider["expectedEveryoneInTheSameGroup"]):
    printOutputMock.assert_called_once()
    for name, _ in vars.tributes.items():
      assert vars.tributes[name]["groupedWith"] == []
  else:
    printOutputMock.assert_not_called()
