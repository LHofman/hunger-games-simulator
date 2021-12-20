import random

import vars

from canPlayEvent import *

def getEvent(tribute, playersRemaining, time, playStandardEvents):
  eventOptions = list(vars.gameData["events"].values())

  #(In/De)crease event odds
  increaseEvents = []
  for (name, value) in list(tribute["statuses"].items()):
    if (
      name not in vars.gameData["statuses"] or
      "increaseEventOdds" not in vars.gameData["statuses"][name]
    ): continue

    increaseEvents.extend(vars.gameData["statuses"][name]["increaseEventOdds"])

  gameSpeed = int(vars.gameData["options"]["speed"])
  if (gameSpeed > 0 and gameSpeed < 11 and gameSpeed != 5):
    diff = abs(gameSpeed - 5)
    multiplier = diff / 5
    percentage = (1 if gameSpeed > 5 else -1) * 100 * multiplier
    for (name, event) in list(vars.gameData["events"].items()):
      if ("deaths" in event):
        increaseEvents.append({"event": name, "percentage": percentage})

  for increaseEvent in increaseEvents:
    percentage = increaseEvent["percentage"]
    if (percentage > 0):
      while (percentage >= 100):
        eventOptions.append(vars.gameData["events"][increaseEvent["event"]])
        percentage -= 100
      rnd = random.random()
      if (rnd < (percentage/100)):
        eventOptions.append(vars.gameData["events"][increaseEvent["event"]])
    else:
      rnd = random.random()
      if (rnd < (abs(percentage)/100)):
        eventOptions.remove(vars.gameData["events"][increaseEvent["event"]])

  eventOptions = list(filter(
    canPlayEvent(tribute, playersRemaining, time, playStandardEvents),
    eventOptions
  ))

  event = random.choice(eventOptions)

  return event
