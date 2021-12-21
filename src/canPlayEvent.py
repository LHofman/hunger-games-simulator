import vars

from utils.possessionUtils import *

def canPlayEvent(tribute, playersRemaining, time, playStandardEvents):
  def canPlayEvent(event):
    if ("ignore" in event): return False

    if ("players" in event and event["players"] > len(playersRemaining) + 1): return False
    if ("formGroup" in event and len(vars.tributes) == 2): return False

    if (not checkHasRequiredPossessions(tribute, event)): return False
    if (not checkCanPlayTimedEvents(time, event, playStandardEvents)): return False
    if (not checkcompliesWithRequiredGroupSize(tribute, event, playersRemaining)): return False
    if (not checkCanBetrayTeammates(tribute, event)): return False

    return True

  return canPlayEvent

def checkHasRequiredPossessions(tribute, event):
  if ("requiresPossessions" not in event): return True

  for possession in event["requiresPossessions"]:
    playerHasPossession = hasPossession(tribute, possession["type"], possession["value"])
    if ("not" in possession and possession["not"]):
      if (playerHasPossession): return False
    else:
      if (not playerHasPossession): return False

  return True

def checkcompliesWithRequiredGroupSize(tribute, event, playersRemaining):
  if ("requireGroupSize" not in event): return True

  sizeType = event["requireGroupSize"]["type"]
  size = event["requireGroupSize"]["amount"]

  availableGroupTributes = 1 # tribute themself
  for (name, player) in playersRemaining.items():
    if (name in tribute["groupedWith"]):
      availableGroupTributes += 1
  
  if (sizeType == "exact" and size != len(tribute["groupedWith"]) + 1): return False
  if (sizeType == "min" and size > availableGroupTributes): return False
  if (sizeType == "max" and size < len(tribute["groupedWith"]) + 1): return False

  return True

def checkCanPlayTimedEvents(time, event, playStandardEvents):
  if ("time" in event):
    timesList = event["time"]
    if (not isinstance(timesList, list)):
      timesList = [timesList]
    if (time not in timesList): return False
  elif (not playStandardEvents): return False

  return True

def checkCanBetrayTeammates(tribute, event):
  if (vars.gameData["options"]["betrayTeammates"]): return True
  if ("deaths" not in event): return True
  if ("killTeammates" not in event or not event["killTeammates"]): return True

  for death in event["deaths"]:
    if (death in tribute["groupedWith"]): return False

  return True