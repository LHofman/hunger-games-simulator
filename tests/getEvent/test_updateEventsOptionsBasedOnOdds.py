import pytest
import random
import vars
from getEvent import updateEventsOptionsBasedOnOdds

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

def test_updateEventsOptionsBasedOnOdds():
  increasedOddsEvents = [
    { "event": "exploreArena", "percentage": 100 },
    { "event": "goHunting", "percentage": 240 },
    { "event": "thinksAboutHome", "percentage": 251 },
    { "event": "prickWhilePickingBerries", "percentage": -40 },
    { "event": "collectFruitFromTree", "percentage": -51 },
    { "event": "discoverRiver", "percentage": -100 },
  ]
  eventOptions = [
    { "name": "exploreArena" },
    { "name": "goHunting" },
    { "name": "thinksAboutHome" },
    { "name": "prickWhilePickingBerries" },
    { "name": "collectFruitFromTree" },
    { "name": "discoverRiver" },
  ]

  updateEventsOptionsBasedOnOdds(
    increasedOddsEvents,
    eventOptions
  )

  assert eventOptions == [
    { "name": "exploreArena" },
    { "name": "goHunting" },
    { "name": "thinksAboutHome" },
    { "name": "prickWhilePickingBerries" },
    { "name": "exploreArena" },
    { "name": "goHunting" },
    { "name": "goHunting" },
    { "name": "thinksAboutHome" },
    { "name": "thinksAboutHome" },
    { "name": "thinksAboutHome" },
  ]
