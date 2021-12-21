import random
import re

import vars;

from utils.possessionUtils import *

def handleEventEffects(event, players, text):
  global recentDeaths

  handleAddPossessions(event, players)
  handleRemovePossessions(event, players)
  text = handleStealItem(event, players, text)
  handleFormGroup(event, players)
  handleSplitGroup(event, players)
  handleDeaths(event, players)

  return text

def handleAddPossessions(event, players):
  if ("addPossessions" not in event): return

  for possession in event["addPossessions"]:
    addPossession(
      vars.tributes[players[possession["player"] - 1]["name"]],
      possession["type"],
      possession["value"]
    )

def handleRemovePossessions(event, players):
  if ("removePossessions" not in event): return

  for possession in event["removePossessions"]:
    removePossession(
      vars.tributes[players[possession["player"] - 1]["name"]],
      possession["type"],
      possession["value"]
    )

def handleStealItem(event, players, text):
  if ("stealItem" not in event): return text

  tribute = players[0]
  item = random.choice(vars.tributes[tribute["name"]]["possessions"]["item"])
  removePossession(vars.tributes[tribute["name"]], "item", item)
  index = int(re.search(r'\d+', event["stealItem"]).group()) - 1
  addPossession(vars.tributes[players[index]["name"]], "item", item)
  return text.replace("(item)", item)

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