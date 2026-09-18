import pytest
import random
from getEventTextPlayersAndTerms import setPossessionsTerms

@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch(
    "random.choice",
    side_effect=lambda list: list[0]
  )

def test_setPossessionsTerms():
  tribute = { "possessions": { "pet": ["cat", "dog"] } }
  text = "Tribute's pet (Possession:pet1) attacks and kills Enemy."

  result = setPossessionsTerms( None, tribute, text, )

  assert result == (
    "Tribute's pet cat attacks and kills Enemy.",
    { "(Possession:pet1)": "cat" }
  )
