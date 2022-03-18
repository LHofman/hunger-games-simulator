import json

import vars

from playGame import *
from utils.generalUtils import *

def readFile(fileName, type = "text"):
  file = open("settings/%s" % fileName, "r", encoding="utf-8")
  
  if (type == 'json'):
    return json.load(file)

  lines = file.readlines()
  return list(map(lambda line: line.rstrip(), lines))

def readTributes():
  file = open("settings/tributes.txt", "r", encoding="utf-8")
  lines = file.readlines()

  if (vars.gameData["options"]["districts"] > 0):
    playersPerDistrict = len(lines) / vars.gameData["options"]["districts"]
  elif (vars.gameData["options"]["playersPerDistrict"] > 0):
    playersPerDistrict = vars.gameData["options"]["playersPerDistrict"]
  else: playersPerDistrict = 0
  
  tributes = {}
  players = 0
  for line in lines:
    players += 1
    name = line.rstrip()
    tributes[name] = {
      "index": players,
      "name": name, 
      "district": int(((players-1)/playersPerDistrict)+1) if (playersPerDistrict > 0) else 0,
      "groupedWith": [],
      "possessions": {}
    }

  if (vars.gameData["options"]["districtsAreTeammates"]):
    for name, tribute in list(tributes.items()):
      for name2, tribute2 in list(tributes.items()):
        if (name2 != name and tribute2["district"] == tribute["district"]):
          tribute["groupedWith"].append(name2)

  return tributes

def getEvents():
  events = {}

  for (name, event) in vars.gameData["events"].items():
    events[name] = { "name": name } | event

  return events


def printWinner():
  if (len(vars.tributes) == 1): printOutput("The winner is %s" % list(vars.tributes.keys())[0])
  elif (len(vars.tributes) > 1): printOutput("The winners are %s" % ", ".join(list(vars.tributes.keys())))
  else: printOutput("There are no winners today")

def printRankings():
  printOutput("\n\n\n---\nFinal Rankings")

  for playerDeaths in vars.deaths:
    for (player, district) in playerDeaths:
      tributeData = vars.tributesData[player]
      printOutput("%d. %s from district %d, died during %s, has %d kills" % (vars.totalTributes, player, district, tributeData["time of death"], tributeData["kills"] if "kills" in tributeData else 0))
      vars.totalTributes -= 1
  
  for name, tribute in list(vars.tributes.items()):
    printOutput("1. %s from district %d" % (name, tribute["district"]))

vars.gameData = readFile("gameData.json", "json")
vars.events = getEvents()
vars.tributes = readTributes()
vars.totalTributes = len(vars.tributes)
vars.sponsors = readFile("sponsors.txt")
vars.deaths = []
vars.recentDeaths = []

if (vars.gameData["options"]["autoPlay"]):
  outputFile = open("resources/output.txt", "w")
  outputFile.write("")
  outputFile.close()

printOutput('----------------------------------------------------------------------------------------------------------------')
playGame()
printWinner()
printRankings()