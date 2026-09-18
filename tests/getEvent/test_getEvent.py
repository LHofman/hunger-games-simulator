import pytest
import random
import vars
from getEvent import getEvent

@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object(
    vars,
    "events",
    {
      "exploreArena": { "name": "exploreArena" },
      "goHunting": { "name": "goHunting" },
      "thinksAboutHome": { "name": "thinksAboutHome" },
      "prickWhilePickingBerries": { "name": "prickWhilePickingBerries" },
      "collectFruitFromTree": { "name": "collectFruitFromTree" },
      "discoverRiver": { "name": "discoverRiver" },
    },
  )
  mocker.patch( "random.random", return_value=0.5 )
  mocker.patch(
    "random.choice",
    side_effect=lambda list: list[0]
  )

  mocker.patch(
    "getEvent.canPlayEvent",
    return_value=lambda event: event["name"] != "exploreArena"
  )
  
  mocker.patch( "getEvent.getIncreasedOddsEventsFromPossessions", return_value=[] )
  mocker.patch( "getEvent.getIncreasedOddsEventsFromGameSpeed", return_value=[] )
  mocker.patch( "getEvent.getDefaultIncreasedOddsEvents", return_value=[] )
  mocker.patch(
    "getEvent.updateEventsOptionsBasedOnOdds",
    side_effect=lambda increasedOddsEvents, eventOptions: eventOptions.remove({"name": "goHunting"})
  )

def test_getEvent():
  eventOptions = [
    { "name": "exploreArena" },
  ]

  result = getEvent( None, None, None, None )

  assert result == { "name": "thinksAboutHome" }
