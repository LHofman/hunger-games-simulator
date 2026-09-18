import pytest
import vars
from playGame import isGameOver

providers = [
  ({
    "id": "Game with 0 tributes left is over",
    "tributes": {},
    "districtCanWinTogether": False,
    "expectedIsGameOver": True,
  }),
  ({
    "id": "Game with 1 tribute left is over",
    "tributes": {"Tribute1": {"name": "Tribute1"}},
    "districtCanWinTogether": False,
    "expectedIsGameOver": True,
  }),
  ({
    "id": "Game with 2 tributes left is not over",
    "tributes": {"Tribute1": {"name": "Tribute1", "district": 1}, "Tribute2": {"name": "Tribute2", "district": 2}},
    "districtCanWinTogether": False,
    "expectedIsGameOver": False,
  }),
  ({
    "id": "Game with 2 tributes left in same district is over when districtCanWinTogether is True",
    "tributes": {"Tribute1": {"name": "Tribute1", "district": 1}, "Tribute2": {"name": "Tribute2", "district": 1}},
    "districtCanWinTogether": True,
    "expectedIsGameOver": True,
  }),
  ({
    "id": "Game with 2 tributes left in same district is not over when districtCanWinTogether is False",
    "tributes": {"Tribute1": {"name": "Tribute1", "district": 1}, "Tribute2": {"name": "Tribute2", "district": 1}},
    "districtCanWinTogether": False,
    "expectedIsGameOver": False,
  }),
  ({
    "id": "Game with 3 tributes left, some in same district is not over",
    "tributes": {"Tribute1": {"name": "Tribute1", "district": 1}, "Tribute2": {"name": "Tribute2", "district": 1}, "Tribute3": {"name": "Tribute3", "district": 2}},
    "districtCanWinTogether": True,
    "expectedIsGameOver": False,
  }),
]

@pytest.mark.parametrize("provider", providers, ids=lambda p: f"{p['id']}")
def test_isGameOver(provider, mocker):
  mocker.patch.object( vars, "gameData", { "options": { "districtCanWinTogether": provider["districtCanWinTogether"] } } )
  mocker.patch.object( vars, "tributes", provider["tributes"] )

  result = isGameOver()

  assert result == provider["expectedIsGameOver"]
