import json
import random
import re

def readFile(fileName, type = "text"):
    file = open(fileName, "r")
    
    if (type == 'json'):
        return json.load(file)

    lines = file.readlines()
    return list(map(lambda line: line.rstrip(), lines))

def readTributes():
    global gameData

    file = open("tributes.txt", "r")
    lines = file.readlines()

    if (gameData["options"]["districts"] > 0):
        playersPerDistrict = len(lines) / gameData["options"]["districts"]
    elif (gameData["options"]["playersPerDistrict"] > 0):
        playersPerDistrict = gameData["options"]["playersPerDistrict"]
    else: playersPerDistrict = 0
    
    tributes = {}
    players = 0
    for line in lines:
        players += 1
        name = line.rstrip()
        tributes[name] = {
            "index": players,
            "name": name, 
            "district": int(((players-1)/playersPerDistrict)+1) if (playersPerDistrict > 0) else 0,
            "items": [],
            "statuses": {},
            "groupedWith": []
        }

    if (gameData["options"]["districtsAreTeammates"]):
        for name, tribute in list(tributes.items()):
            for name2, tribute2 in list(tributes.items()):
                if (name2 != name and tribute2["district"] == tribute["district"]):
                    tribute["groupedWith"].append(name2)

    return tributes

def percentageOfPlaying(total, time):
    if (time in ["bloodbath", "feast"]): return 1
    
    if (total > 25): return 15/total
    if (total > 15): return 0.5
    if (total > 5): return 0.75
    return 1

def playList(time, playStandardEvents):
    global tributes
    
    tributesLeft = tributes.copy()
    played = 0
    total = amountLeft = len(tributesLeft)
    while (amountLeft > 0 and len(tributes) > 1):
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
        playList(tributes)

def playTribute(tribute, playersRemaining, time, playStandardEvents):
    event = getEvent(tribute, playersRemaining, time, playStandardEvents)

    (text, players) = getEventTextAndPlayers(event, tribute, playersRemaining)
    
    text = handleEventEffects(event, players, text)
    
    print(text)

def getEvent(tribute, playersRemaining, time, playStandardEvents):
    global gameData

    eventOptions = list(gameData["events"].values())

    #(In/De)crease event odds
    for (name, value) in list(tribute["statuses"].items()):
        if (
            name not in gameData["statuses"] or
            "increaseEventOdds" not in gameData["statuses"][name]
        ): continue

        for increaseEvent in gameData["statuses"][name]["increaseEventOdds"]:
            percentage = increaseEvent["percentage"]
            if (percentage > 0):
                while (percentage >= 100):
                    eventOptions.append(gameData["events"][increaseEvent["event"]])
                    percentage -= 100
                rnd = random.random()
                if (rnd < (percentage/100)):
                    eventOptions.append(gameData["events"][increaseEvent["event"]])
            else:
                rnd = random.random()
                if (rnd < (abs(percentage)/100)):
                    eventOptions.remove(gameData["events"][increaseEvent["event"]])

    eventOptions = list(filter(
        canPlayEvent(tribute, playersRemaining, time, playStandardEvents),
        eventOptions
    ))

    event = random.choice(eventOptions)

    return event

def canPlayEvent(tribute, playersRemaining, time, playStandardEvents):
    global gameData
    global sponsors

    def canPlayEvent(event):
        if ("players" in event and event["players"] > len(playersRemaining)+1): return False
        if ("addItem" in event and event["addItem"] in tribute["items"]): return False
        if ("formGroup" in event and len(tributes) == 2): return False

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
            not gameData["options"]["betrayTeammates"] and "deaths" in event and
            ("killTeammates" not in event or not event["killTeammates"])
        ):
            for death in event["deaths"]:
                if (death in tribute["groupedWith"]): return False

        return True

    return canPlayEvent

def checkEveryoneInTheSameGroup():
    global tributes

    for name, tribute in tributes.items():
        for name2, tribute2 in tributes.items():
            if (name2 != name and name2 not in tribute["groupedWith"]): return

    for name, _ in tributes.items():
        tributes[name]["groupedWith"].clear()

    print("The remaining tributes realize they are the only ones left and split up")

def getEventTextAndPlayers(event, tribute, playersRemaining):
    global gameData
    global sponsors
    global totalTributes
    global tributes
    
    # Find players grouped with tribute needed for event
    if ("requireGroupSize" in event):
        aoGroupPlayersRequired = event["requireGroupSize"]["amount"]

        groupedWithPlayers = {}
        for (name, player) in playersRemaining.items():
            if (name in tribute["groupedWith"]):
                groupedWithPlayers[name] = player
    else: aoGroupPlayersRequired = 0

    # Set players' names in event
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

    # Set sponsor's name in event
    if (text.find("(Sponsor)") > -1):
        if (len(sponsors) > 0):
            isFixedSponsor = gameData["options"]["1SponsorPerTribute"]
            if (isFixedSponsor and len(sponsors) == totalTributes):
                sponsor = sponsors[tribute["index"] - 1]
            else:
                sponsor = random.choice(sponsors)
        else: sponsor = "an unknown sponsor"

        text = text.replace("(Sponsor)", sponsor)

    return (text, players)

def handleEventEffects(event, players, text):
    global tributes
    global recentDeaths

    tribute = players[0]

    if ("addItem" in event):
        tributes[tribute["name"]]["items"].append(event["addItem"])

    if ("stealItem" in event):
        item = random.choice(tributes[tribute["name"]]["items"])
        tributes[tribute["name"]]["items"].remove(item)
        index = int(re.search(r'\d+', event["stealItem"]).group()) - 1
        tributes[players[index]["name"]]["items"].append(item)
        text = text.replace("(item)", item)

    if ("setStatus" in event):
        for player in event["setStatus"]["players"]:
            index = int(re.search(r'\d+', player).group()) - 1
            tributes[players[index]["name"]]["statuses"][event["setStatus"]["status"]] = event["setStatus"]["value"]

    if ("formGroup" in event):
        for player in players:
            for otherPlayer in players:
                if (player["name"] == otherPlayer["name"]): continue
                if (otherPlayer["name"] in tributes[player["name"]]["groupedWith"]): continue
                tributes[player["name"]]["groupedWith"].append(otherPlayer["name"])

    if ("splitGroup" in event):
        playersToSplit = []
        for playerToSplit in event["splitGroup"]:
            index = int(re.search(r'\d+', playerToSplit).group()) - 1
            playersToSplit.append(players[index]["name"])
            
        for player in players:
            if (player["name"] not in playersToSplit): continue
            for playerToSplit in playersToSplit:
                if (playerToSplit != player["name"]):
                    tributes[player["name"]]["groupedWith"].remove(playerToSplit)

    if ("deaths" in event):
        for death in event["deaths"]:
            index = int(re.search(r'\d+', death).group()) - 1
            playerName = players[index]["name"]
            recentDeaths.append((playerName, players[index]["district"]))

            for (name, _tribute) in tributes.items():
                if playerName in _tribute["groupedWith"]:
                    tributes[name]["groupedWith"].remove(playerName)

            del tributes[playerName]

    return text


def playGame():
    global tributes

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

def isGameOver():
    global gameData
    global tributes

    if (len(tributes) <= 1): return True

    if (gameData["options"]["districtCanWinTogether"]):
        isEveryoneInSameDistrict = True
        for name, tribute in tributes.items():
            for name2, tribute2 in tributes.items():
                if (name2 != name and tribute2["district"] != tribute["district"]):
                    isEveryoneInSameDistrict = False
                    break
            if (not isEveryoneInSameDistrict): break
    
        if (isEveryoneInSameDistrict): return True

    return False

def readInput():
    global tributes

    userInput = input("Press Enter to continue, or type status to see the current status of all tributes: ")
    print("")

    if (userInput == "stop"): exit()

    if (userInput == "status"):
        printStatus()
        readInput()

def printStatus():
    global tributes

    for (name, tribute) in tributes.items():
        print("%s from district %d is still alive%s%s%s" % (
            name,
            tribute["district"],
            "" if (len(tribute["statuses"]) == 0) else (
                ", is: " + ", ".join(list(tribute["statuses"].keys()))
            ),
            "" if (len(tribute["items"]) == 0) else (
                ", has: " + ", ".join(tribute["items"])
            ),
            "" if (len(tribute["groupedWith"]) == 0) else (
                ", is in a group with: " + ", ".join(tribute["groupedWith"])
            ),
        ))

    print("\n---")

def shuffleTributes():
    global tributes
    l = list(tributes.items())
    random.shuffle(l)
    tributes = dict(l)

def showFallenTributes():
    global gameData
    global deaths
    global recentDeaths

    if (len(recentDeaths) > 0 and gameData["options"]["showFallenTributes"]):
        if (not isGameOver()): readInput()
        print("%d cannon shots can be heard in the distance." % len(recentDeaths))
        for playerName, district in recentDeaths:
            print ("%s from district %d" % (playerName, district))
        print("---")
    
    deaths.append(recentDeaths.copy())
    recentDeaths.clear()


def printWinner():
    global tributes

    if (len(tributes) == 1): print("The winner is %s" % list(tributes.keys())[0])
    elif (len(tributes) > 1): print("The winners are %s" % ", ".join(list(tributes.keys())))
    else: print("There are no winners today")

def printRankings():
    global deaths
    global totalTributes
    global tributes

    print("\n\n\n---\nFinal Rankings")

    for playerDeaths in deaths:
        for (player, district) in playerDeaths:
            print("%d. %s from district %d" % (totalTributes, player, district))
            totalTributes -= 1
    
    for name, tribute in list(tributes.items()):
        print("1. %s from district %d" % (name, tribute["district"]))

print('----------------------------------------------------------------------------------------------------------------')
gameData = readFile("gamedata.json", "json")
tributes = readTributes()
totalTributes = len(tributes)
sponsors = readFile("sponsors.txt")
deaths = []
recentDeaths = []

playGame()
printWinner()
printRankings()
