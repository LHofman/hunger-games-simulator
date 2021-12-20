import random
import re

import vars;

def handleEventEffects(event, players, text):
  global recentDeaths

  tribute = players[0]

  if ("addItem" in event):
    vars.tributes[tribute["name"]]["items"].append(event["addItem"])

  if ("stealItem" in event):
    item = random.choice(vars.tributes[tribute["name"]]["items"])
    vars.tributes[tribute["name"]]["items"].remove(item)
    index = int(re.search(r'\d+', event["stealItem"]).group()) - 1
    vars.tributes[players[index]["name"]]["items"].append(item)
    text = text.replace("(item)", item)

  if ("setStatus" in event):
    for player in event["setStatus"]["players"]:
      index = int(re.search(r'\d+', player).group()) - 1
      vars.tributes[players[index]["name"]]["statuses"][event["setStatus"]["status"]] = event["setStatus"]["value"]

  if ("formGroup" in event):
    for player in players:
      for otherPlayer in players:
        if (player["name"] == otherPlayer["name"]): continue
        if (otherPlayer["name"] in vars.tributes[player["name"]]["groupedWith"]): continue
        vars.tributes[player["name"]]["groupedWith"].append(otherPlayer["name"])

  if ("splitGroup" in event):
    playersToSplit = []
    for playerToSplit in event["splitGroup"]:
      index = int(re.search(r'\d+', playerToSplit).group()) - 1
      playersToSplit.append(players[index]["name"])
      
    for player in players:
      if (player["name"] not in playersToSplit): continue
      for playerToSplit in playersToSplit:
        if (playerToSplit != player["name"]):
          vars.tributes[player["name"]]["groupedWith"].remove(playerToSplit)

  if ("deaths" in event):
    for death in event["deaths"]:
      index = int(re.search(r'\d+', death).group()) - 1
      playerName = players[index]["name"]
      vars.recentDeaths.append((playerName, players[index]["district"]))

      for (name, _tribute) in vars.tributes.items():
        if playerName in _tribute["groupedWith"]:
          vars.tributes[name]["groupedWith"].remove(playerName)

      del vars.tributes[playerName]

  return text
