import json
from typing import TypedDict, Union

from Application.GameExecutor import GameExecutor
from Application.Printer import Printer
from Domain.types import Event, GameConfig, GameOptions, GameState, IncreaseEventOddsMap, Tribute

printer: Printer = Printer()

def readFile(fileName: str, type: str = 'text') -> Union[dict, list, None]: # type: ignore
  file = open(fileName, 'r', encoding='utf-8')
  
  if (type == 'json'):
    return json.load(file)

  lines = file.readlines()
  return list(map(lambda line: line.rstrip(), lines))

def readTributes(gameOptions: GameOptions, tributesFileName: str) -> dict[str, Tribute]:
  file = open(tributesFileName, 'r', encoding='utf-8')
  lines = file.readlines()

  if (gameOptions['districts'] > 0):
    playersPerDistrict = len(lines) / gameOptions['districts']
  elif (gameOptions['playersPerDistrict'] > 0):
    playersPerDistrict = gameOptions['playersPerDistrict']
  else: playersPerDistrict = 0
  
  tributes: dict[str, Tribute] = {}
  players = 0
  for line in lines:
    players += 1
    name = line.rstrip()
    tributes[name] = {
      'index': players,
      'name': name, 
      'district': int(((players-1)/playersPerDistrict)+1) if (playersPerDistrict > 0) else 0,
      'groupedWith': [],
      'possessions': {}
    }

  if (gameOptions['districtsAreTeammates']):
    for name, tribute in list(tributes.items()):
      for name2, tribute2 in list(tributes.items()):
        if (name2 != name and tribute2['district'] == tribute['district']):
          tribute['groupedWith'].append(name2)

  return tributes

def addNameToEvents(events: dict[str, Event]) -> dict[str, Event]:
  for (name, event) in events.items():
    event['name'] = name
    events[name] = event
    
  return events

def printWinner(gameState: GameState, printer: Printer):
  if (len(gameState['playersAlive']) == 1):
    printer.print('The winner is %s' % list(gameState['playersAlive'].keys())[0])
  elif (len(gameState['playersAlive']) > 1):
    printer.print('The winners are %s' % ', '.join(list(gameState['playersAlive'].keys())))
  else:
    printer.print('There are no winners today')

def printRankings(gameState: GameState, printer: Printer):
  printer.print('\n\n\n---\nFinal Rankings')

  for playerDeaths in gameState['deaths']:
    for (player, district) in playerDeaths:
      tributeData = gameState['tributesData'][player]
      printer.print('%d. %s from district %d, died during %s, has %d kills' % (
        gameState['totalTributes'],
        player,
        district,
        tributeData['time of death'],
        tributeData['kills'] if 'kills' in tributeData else 0
      ))
      gameState['totalTributes'] -= 1

  for name, tribute in list(gameState['playersAlive'].items()):
    printer.print('1. %s from district %d' % (name, tribute['district']))

class GameDataFile(TypedDict):
  options: GameOptions
  increaseEventOdds: IncreaseEventOddsMap
  events: dict[str, Event]
  replaceTerms: dict[str, list[str]]

gameDataFile: GameDataFile = readFile('settings/gameData.json', 'json') # type: ignore

if (gameDataFile['options']['autoPlay']):
  from Application.Printers.FilePrinter import FilePrinter
  printer = FilePrinter('resources/output.txt')

tributes = readTributes(gameDataFile['options'], 'settings/tributes.txt')
sponsors: list[str] = readFile('settings/sponsors.txt') # type: ignore

if (gameDataFile['options']['autoPlay']):
  outputFile = open('resources/output.txt', 'w')
  outputFile.write('')
  outputFile.close()

printer.print('----------------------------------------------------------------------------------------------------------------')

gameState: GameConfig = {
  'options': gameDataFile['options'],
  'otherTerms': gameDataFile['replaceTerms'],
  'sponsors': sponsors,
  'totalTributes': len(tributes),
  'allTributes': tributes,
  'events': addNameToEvents(gameDataFile['events']),
  'increaseEventOdds': gameDataFile['increaseEventOdds'],
}

gameExecutor = GameExecutor(gameState, printer)
finalGameState = gameExecutor.playGame()

printWinner(finalGameState, printer)
printRankings(finalGameState, printer)