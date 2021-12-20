import vars

def canPlayEvent(tribute, playersRemaining, time, playStandardEvents):
  def canPlayEvent(event):
    if ("players" in event and event["players"] > len(playersRemaining)+1): return False
    if ("addItem" in event and event["addItem"] in tribute["items"]): return False
    if ("formGroup" in event and len(vars.tributes) == 2): return False

    if ("requiresStatus" in event and (
      event["requiresStatus"] not in tribute["statuses"] or
      not tribute["statuses"][event["requiresStatus"]]
    )): return False

    if ("time" in event):
      timesList = event["time"]
      if (not isinstance(timesList, list)):
        timesList = [timesList]
      if (time not in timesList): return False
    elif (not playStandardEvents): return False

    if ("requiresItem" in event and event["requiresItem"] not in tribute["items"]):
      if (event["requiresItem"] != "anyItem" or len(tribute["items"]) == 0): return False

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
