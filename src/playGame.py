import random

import vars

from getEvent import *
from getEventTextAndPlayers import *
from handleEventEffects import *
from utils.possessionUtils import *

def playGame():
  playRound("The Bloodbath", "bloodbath", False)
  day = 0
  while (not isGameOver()):
    day += 1
    playRound("Day %d" % day, "day", True)
    showFallenTributes()
    playRound("Night %d" % day, "night", True)
    if (day == 5): playRound("The Feast", "feast", False)

def playRound(text, time, playStandardEvents):
  if (isGameOver()): return

  shuffleTributes()
  readInput()
  print(text)
  playList(time, playStandardEvents)
  print('\n---')

def playList(time, playStandardEvents):
  tributesLeft = vars.tributes.copy()
  played = 0
  total = amountLeft = len(tributesLeft)
  while (amountLeft > 0 and len(vars.tributes) > 1):
    checkEveryoneInTheSameGroup()

    tribute = list(tributesLeft.values())[0]
    del tributesLeft[tribute["name"]]
    percentage = percentageOfPlaying(total, time)
    rnd = random.random()
    if (rnd < percentage):
      playTribute(tribute, tributesLeft, time, playStandardEvents)
      played += 1
      
    amountLeft = len(tributesLeft)

  if (played == 0):
    playList(vars.tributes)

def playTribute(tribute, playersRemaining, time, playStandardEvents):
  event = getEvent(tribute, playersRemaining, time, playStandardEvents)

  (text, players) = getEventTextAndPlayers(event, tribute, playersRemaining)
  
  text = handleEventEffects(event, players, text)
  
  print(text)

def readInput():
  userInput = input("Press Enter to continue, or type status to see the current status of all tributes: ")
  print("")

  if (userInput == "stop"): exit()

  if (userInput == "status"):
    printStatus()
    readInput()

def isGameOver():
  if (len(vars.tributes) <= 1): return True

  if (vars.gameData["options"]["districtCanWinTogether"]):
    isEveryoneInSameDistrict = True
    for name, tribute in vars.tributes.items():
      for name2, tribute2 in vars.tributes.items():
        if (name2 != name and tribute2["district"] != tribute["district"]):
          isEveryoneInSameDistrict = False
          break
      if (not isEveryoneInSameDistrict): break
  
    if (isEveryoneInSameDistrict): return True

  return False

def shuffleTributes():
  l = list(vars.tributes.items())
  random.shuffle(l)
  vars.tributes = dict(l)

def percentageOfPlaying(total, time):
  if (time in ["bloodbath", "feast"]): return 1
  
  if (total > 25): return 15/total
  if (total > 15): return 0.5
  if (total > 5): return 0.75
  return 1

def checkEveryoneInTheSameGroup():
  for name, tribute in vars.tributes.items():
    for name2, tribute2 in vars.tributes.items():
      if (name2 != name and name2 not in tribute["groupedWith"]): return

  for name, _ in vars.tributes.items():
    vars.tributes[name]["groupedWith"].clear()

  print("The remaining tributes realize they are the only ones left and split up")

def showFallenTributes():
  if (len(vars.recentDeaths) > 0 and vars.gameData["options"]["showFallenTributes"]):
    if (not isGameOver()): readInput()
    print("%d cannon shots can be heard in the distance." % len(vars.recentDeaths))
    for playerName, district in vars.recentDeaths:
      print ("%s from district %d" % (playerName, district))
    print("---")
  
  vars.deaths.append(vars.recentDeaths.copy())
  vars.recentDeaths.clear()

def printStatus():
  for (name, tribute) in vars.tributes.items():
    print("%s from district %d is still alive%s%s%s" % (
      name,
      tribute["district"],
      "" if (len(tribute["statuses"]) == 0) else (
        ", is: " + ", ".join(list(tribute["statuses"].keys()))
      ),
      "" if (not hasPossession(tribute, "item", "any")) else (
        ", has: " + ", ".join(tribute["possessions"]["item"])
      ),
      "" if (len(tribute["groupedWith"]) == 0) else (
        ", is in a group with: " + ", ".join(tribute["groupedWith"])
      ),
    ))

  print("\n---")
