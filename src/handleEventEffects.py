import random
import re

import vars;

from utils.possessionUtils import *

def handleEventEffects(event, players, text, terms):
  global recentDeaths

  handleAddPossessions(event, players, terms)
  handleRemovePossessions(event, players, terms)
  handleFormGroup(event, players)
  handleSplitGroup(event, players)
  handleDeaths(event, players)

  return text

def handleAddPossessions(event, players, terms):
  if ("addPossessions" not in event): return

  for possession in event["addPossessions"]:
    value = possession["value"]
    if (value in terms):
      value = terms[value]

    addPossession(
      vars.tributes[players[possession["player"] - 1]["name"]],
      possession["type"],
      value
    )

def handleRemovePossessions(event, players, terms):
  if ("removePossessions" not in event): return

  for possession in event["removePossessions"]:
    value = possession["value"]
    if (value in terms):
      value = terms[value]

    removePossession(
      vars.tributes[players[possession["player"] - 1]["name"]],
      possession["type"],
      value
    )

def handleFormGroup(event, players):
  if ("formGroup" not in event): return

  for player in players:
    for otherPlayer in players:
      if (player["name"] == otherPlayer["name"]): continue
      if (otherPlayer["name"] in vars.tributes[player["name"]]["groupedWith"]): continue
      vars.tributes[player["name"]]["groupedWith"].append(otherPlayer["name"])

def handleSplitGroup(event, players):
  if ("splitGroup" not in event): return

  playersToSplit = []
  for playerToSplit in event["splitGroup"]:
    index = int(re.search(r'\d+', playerToSplit).group()) - 1
    playersToSplit.append(players[index]["name"])
    
  for player in players:
    if (player["name"] not in playersToSplit): continue
    for playerToSplit in playersToSplit:
      if (playerToSplit != player["name"]):
        vars.tributes[player["name"]]["groupedWith"].remove(playerToSplit)

def handleDeaths(event, players):
  if ("deaths" not in event): return

  for death in event["deaths"]:
    index = int(re.search(r'\d+', death).group()) - 1
    playerName = players[index]["name"]
    vars.recentDeaths.append((playerName, players[index]["district"]))

    for (name, _tribute) in vars.tributes.items():
      if playerName in _tribute["groupedWith"]:
        vars.tributes[name]["groupedWith"].remove(playerName)

    del vars.tributes[playerName]