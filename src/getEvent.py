import random

import vars

from canPlayEvent import *

def getEvent(tribute, playersRemaining, time, playStandardEvents):
  eventOptions = list(vars.gameData["events"].values())

  #(In/De)crease event odds
  increaseOddsEvents = []
  increaseOddsEvents.extend(getIncreasedOddsEventsFromPossessions(tribute))
  increaseOddsEvents.extend(getIncreasedOddsEventsFromGameSpeed())

  updateEventsOptionsBasedOnOdds(increaseOddsEvents, eventOptions)

  #Remove events unable to occur at this moment
  eventOptions = list(filter(
    canPlayEvent(tribute, playersRemaining, time, playStandardEvents),
    eventOptions
  ))

  #Get random event
  event = random.choice(eventOptions)

  return event

def getIncreasedOddsEventsFromPossessions(tribute):
  increasedOddsEventsOptions = vars.gameData["increaseEventOdds"]["possessions"]

  increasedOddsEvents = []
  for (type, values) in tribute["possessions"].items():
    if (type not in increasedOddsEventsOptions): continue

    for value in values:
      if (value in increasedOddsEventsOptions[type]):
        increasedOddsEvents.extend(increasedOddsEventsOptions[type][value])

  return increasedOddsEvents

def getIncreasedOddsEventsFromGameSpeed():
  increasedOddsEvents = []

  gameSpeed = int(vars.gameData["options"]["speed"])
  if (gameSpeed < 1 or gameSpeed > 10 or gameSpeed == 5):
    return []

  diff = abs(gameSpeed - 5)
  multiplier = diff / 5
  percentage = (1 if gameSpeed > 5 else -1) * 100 * multiplier
  for (name, event) in list(vars.gameData["events"].items()):
    if ("deaths" in event):
      increasedOddsEvents.append({"event": name, "percentage": percentage})
  
  return increasedOddsEvents

def updateEventsOptionsBasedOnOdds(increasedOddsEvents, eventOptions):
  for increaseEvent in increasedOddsEvents:
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