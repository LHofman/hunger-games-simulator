import random

import vars

from getEvent import *
from getEventTextPlayersAndTerms import *
from handleEventEffects import *
from utils.generalUtils import *
from utils.possessionUtils import *
from utils.tributesDataUtils import *

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
  printOutput(text)
  playList(time, playStandardEvents, text)
  printOutput('\n---')

def playList(time, playStandardEvents, exactTime):
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
      playTribute(tribute, tributesLeft, time, playStandardEvents, exactTime)
      played += 1
      
    amountLeft = len(tributesLeft)

  if (played == 0):
    playList(vars.tributes, playStandardEvents, exactTime)

def playTribute(tribute, playersRemaining, time, playStandardEvents, exactTime):
  event = getEvent(tribute, playersRemaining, time, playStandardEvents)

  (text, players, terms) = getEventTextPlayersAndTerms(event, tribute, playersRemaining)
  
  text = handleEventEffects(event, players, text, terms, exactTime)
  
  printOutput(text)

def readInput():
  if (vars.gameData["options"]["autoPlay"]):
    printOutput("")
    printStatus()
    return

  userInput = input("Press Enter to continue, or type status to see the current status of all tributes: ")
  printOutput("")

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

  printOutput("The remaining tributes realize they are the only ones left and split up")

def showFallenTributes():
  if (len(vars.recentDeaths) > 0 and vars.gameData["options"]["showFallenTributes"]):
    if (not isGameOver()): readInput()
    printOutput("%d cannon shots can be heard in the distance." % len(vars.recentDeaths))
    for playerName, district in vars.recentDeaths:
      printOutput("%s from district %d" % (playerName, district))
    printOutput("---")
  
  vars.deaths.append(vars.recentDeaths.copy())
  vars.recentDeaths.clear()

def printStatus():
  for (name, tribute) in sorted(list(vars.tributes.items())):
    possessions = ''
    for (type, values) in tribute["possessions"].items():
      if (hasPossession(tribute, type, "any")):
        possessions = "%s%s: %s, " % (possessions, type, ", ".join(values))

    if (possessions):
      possessions = ", has %s" % possessions[0: -2]

    printOutput("%s from district %d is still alive%s" % (name, tribute["district"], possessions))

  printOutput("\n---")
