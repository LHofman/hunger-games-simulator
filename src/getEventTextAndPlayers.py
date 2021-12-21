import random

import vars

def getEventTextAndPlayers(event, tribute, playersRemaining):
  # Find players grouped with tribute needed for event
  (aoGroupPlayersRequired, groupedWithPlayers) = getGroupRequiredSizeAndPlayers(
    event,
    tribute,
    playersRemaining
  )

  # Set players' names in event
  (players, text) = setPlayersNames(
    event,
    tribute,
    playersRemaining,
    aoGroupPlayersRequired,
    groupedWithPlayers
  )

  text = setSponsorsNames(tribute, text)

  return (text, players)

def getGroupRequiredSizeAndPlayers(event, tribute, playersRemaining):
  if ("requireGroupSize" not in event): return (0, {})

  aoGroupPlayersRequired = event["requireGroupSize"]["amount"]
  
  groupedWithPlayers = {}
  for (name, player) in playersRemaining.items():
    if (name in tribute["groupedWith"]):
      groupedWithPlayers[name] = player

  return (aoGroupPlayersRequired, groupedWithPlayers)

def setPlayersNames(event, tribute, playersRemaining, aoGroupPlayersRequired, groupedWithPlayers):
  text = event["text"]
  players = []
  while (text.find("(Player") > -1):
    if (len(players) == 0):
      player = tribute
    elif (len(players) < aoGroupPlayersRequired):
      player = random.choice(list(groupedWithPlayers.values()))
      del groupedWithPlayers[player["name"]]
      del playersRemaining[player["name"]]
    else:
      player = random.choice(list(playersRemaining.values()))
      del playersRemaining[player["name"]]
    
    players.append(player)
    text = text.replace("(Player%d)" % len(players), player["name"])

  return (players, text)

def setSponsorsNames(tribute, text):
  if (text.find("(Sponsor)") == -1): return text

  if (len(vars.sponsors) > 0):
    isFixedSponsor = vars.gameData["options"]["1SponsorPerTribute"]
    if (isFixedSponsor and len(vars.sponsors) == vars.totalTributes):
      sponsor = vars.sponsors[tribute["index"] - 1]
    else:
      sponsor = random.choice(vars.sponsors)
  else: sponsor = "an unknown sponsor"

  return text.replace("(Sponsor)", sponsor)