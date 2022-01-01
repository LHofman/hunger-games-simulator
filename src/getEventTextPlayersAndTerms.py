from os import replace
import random
import re

import vars

def getEventTextPlayersAndTerms(event, tribute, playersRemaining):
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

  (text, terms) = setPossessionsTerms(event, tribute, text)
  (text, otherTerms) = setOtherTerms(event, text)
  terms.update(otherTerms)

  text = setSponsorsNames(tribute, text)

  return (text, players, terms)

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

def setPossessionsTerms(event, tribute, text):
  terms = {}
  index = text.find("(Possession:")
  while (index > -1):
    match = re.search(r"\d", text[index:])
    number = int(match.group())
    numberIndex = match.start()

    type = text[(index + len("(Possession:")) : (index + numberIndex)]
    possession = random.choice(tribute["possessions"][type])
    term = "(Possession:%s%d)" % (type, number)
    terms[term] = possession

    text = text.replace(term, possession)

    index = text.find("(Possession:")

  return (text, terms)

def setOtherTerms(event, text):
  terms = {}
  for (key, values) in vars.gameData["replaceTerms"].items():
    index = text.find("(%s" % key)
    while (index > -1):
      number = int(re.search(r"\d", text[index:]).group())
      term = "(%s%d)" % (key, number)

      value = random.choice(values)
      terms[term] = value

      text = text.replace(term, value)

      index = text.find("(%s" % key)

  return (text, terms)

def setSponsorsNames(tribute, text):
  if (text.find("(Sponsor") == -1): return text

  if (len(vars.sponsors) <= 0): return text.replace("(Sponsor)", "an unknown sponsor")

  isFixedSponsor = vars.gameData["options"]["1SponsorPerTribute"]
  if (not isFixedSponsor or  len(vars.sponsors) != vars.totalTributes):
    return text.replace("(Sponsor)", random.choice(vars.sponsors))

  if (text.find("(Sponsor::opposing)") == -1): return text.replace("(Sponsor)", vars.sponsors[tribute["index"] - 1])
  
  sponsorIndex = tribute["index"] - 1
  otherSponsors = vars.sponsors[:sponsorIndex] + vars.sponsors[sponsorIndex+1:]
  return text.replace("(Sponsor::opposing)", random.choice(otherSponsors))