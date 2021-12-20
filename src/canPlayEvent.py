import vars

from utils.possessionUtils import *

def canPlayEvent(tribute, playersRemaining, time, playStandardEvents):
  def canPlayEvent(event):
    if ("ignore" in event): return False

    if ("players" in event and event["players"] > len(playersRemaining)+1): return False
    if ("formGroup" in event and len(vars.tributes) == 2): return False

    if (not checkCanAddPossessions(tribute, event)): return False
    if (not checkCanRemovePossessions(tribute, event)): return False
    if (not checkHasRequiredPossessions(tribute, event)): return False

    if ("time" in event):
      timesList = event["time"]
      if (not isinstance(timesList, list)):
        timesList = [timesList]
      if (time not in timesList): return False
    elif (not playStandardEvents): return False

    if ("requireGroupSize" in event):
      sizeType = event["requireGroupSize"]["type"]
      size = event["requireGroupSize"]["amount"]

      availableGroupTributes = 1 # tribute themself
      for (name, player) in playersRemaining.items():
        if (name in tribute["groupedWith"]):
          availableGroupTributes += 1
      
      if (sizeType == "exact" and size != len(tribute["groupedWith"]) + 1): return False
      if (sizeType == "min" and size > availableGroupTributes): return False
      if (sizeType == "max" and size < len(tribute["groupedWith"]) + 1): return False

    if (
      not vars.gameData["options"]["betrayTeammates"] and "deaths" in event and
      ("killTeammates" not in event or not event["killTeammates"])
    ):
      for death in event["deaths"]:
        if (death in tribute["groupedWith"]): return False

    return True

  return canPlayEvent

# TODO: add possessions to other tributes
def checkCanAddPossessions(tribute, event):
  if ("addPossessions" not in event): return True

  for possession in event["addPossessions"]:
    if (hasPossession(tribute, possession["type"], possession["value"])): return False

  return True

# TODO: remove possessions from other tributes
def checkCanRemovePossessions(tribute, event):
  if ("removePossessions" not in event): return True

  for possession in event["removePossessions"]:
    if (not hasPossession(tribute, possession["type"], possession["value"])): return False

  return True

# TODO: require possessions from other tributes
def checkHasRequiredPossessions(tribute, event):
  if ("requiresPossessions" not in event): return True

  for possession in event["requiresPossessions"]:
    if (not hasPossession(tribute, possession["type"], possession["value"])): return False

  return True