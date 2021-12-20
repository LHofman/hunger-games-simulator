import json

import vars

from playGame import *

def readFile(fileName, type = "text"):
  file = open("settings/%s" % fileName, "r")
  
  if (type == 'json'):
    return json.load(file)

  lines = file.readlines()
  return list(map(lambda line: line.rstrip(), lines))

def readTributes():
  file = open("settings/tributes.txt", "r")
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


def printWinner():
  if (len(vars.tributes) == 1): print("The winner is %s" % list(vars.tributes.keys())[0])
  elif (len(vars.tributes) > 1): print("The winners are %s" % ", ".join(list(vars.tributes.keys())))
  else: print("There are no winners today")

def printRankings():
  print("\n\n\n---\nFinal Rankings")

  for playerDeaths in vars.deaths:
    for (player, district) in playerDeaths:
      print("%d. %s from district %d" % (vars.totalTributes, player, district))
      vars.totalTributes -= 1
  
  for name, tribute in list(vars.tributes.items()):
    print("1. %s from district %d" % (name, tribute["district"]))

print('----------------------------------------------------------------------------------------------------------------')
vars.gameData = readFile("gameData.json", "json")
vars.tributes = readTributes()
vars.totalTributes = len(vars.tributes)
vars.sponsors = readFile("sponsors.txt")
vars.deaths = []
vars.recentDeaths = []


playGame()
printWinner()
printRankings()
