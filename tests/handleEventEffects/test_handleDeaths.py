from Domain.EventRules.Deaths import Deaths
from Domain.EventRule import TextAndTerms
from Domain.types import GameRoundState
from tests.defaults import (
  defaultEvent,
  defaultGameRoundState,
  defaultTribute,
)

def test_handleDeaths():
  gameState: GameRoundState = {
    **defaultGameRoundState,
    'event': {
      **defaultEvent,
      'deaths': ['Player2', 'Player3']
    },
    'playersAlive': {
      'Tribute1': { **defaultTribute, 'name': 'Tribute1', 'district': 1, 'groupedWith': ['Tribute2', 'Tribute3'] },
      'Tribute2': { **defaultTribute, 'name': 'Tribute2', 'district': 2, 'groupedWith': ['Tribute1'] },
      'Tribute3': { **defaultTribute, 'name': 'Tribute3', 'district': 3, 'groupedWith': ['Tribute1'] },
    },
    'exactTime': 'day',
  }

  textAndTerms: TextAndTerms = {
    'text': '',
    'players': [
      { **defaultTribute, 'name': 'Tribute1', 'district': 1, 'groupedWith': ['Tribute2', 'Tribute3'] },
      { **defaultTribute, 'name': 'Tribute2', 'district': 2, 'groupedWith': ['Tribute1'] },
      { **defaultTribute, 'name': 'Tribute3', 'district': 3, 'groupedWith': ['Tribute1'] },
    ]
  }

  Deaths().handleEventEffects(
    gameState,
    textAndTerms
  )

  assert gameState['recentDeaths'] == [('Tribute2', 2), ('Tribute3', 3)]
  assert gameState['tributesData']['Tribute2']['time of death'] == 'day'
  assert gameState['tributesData']['Tribute2']['district'] == 2
  assert gameState['tributesData']['Tribute3']['time of death'] == 'day'
  assert gameState['tributesData']['Tribute3']['district'] == 3
  assert gameState['playersAlive'] == {
    'Tribute1': { **defaultTribute, 'name': 'Tribute1', 'district': 1, 'groupedWith': [] },
  }