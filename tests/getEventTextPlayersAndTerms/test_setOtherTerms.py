import pytest
import random
import vars
from getEventTextPlayersAndTerms import setOtherTerms

@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object(
    vars,
    "gameData",
    { "replaceTerms": { "Animal": ["cat", "dog"] } }
  )

  mocker.patch(
    "random.choice",
    side_effect=lambda list: list[0]
  )

def test_setOtherTerms():
  result = setOtherTerms(
    None,
    "Tribute finds a (Animal1), They pet it and the (Animal1) follows them around",
  )

  assert result == (
    "Tribute finds a cat, They pet it and the cat follows them around",
    { "(Animal1)": "cat" }
  )
