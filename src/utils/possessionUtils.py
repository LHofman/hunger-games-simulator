import vars

def addPossession(tribute, type, value):
  if (type in tribute["possessions"]):
    if (type not in vars.gameData["options"]["possessionsWithoutDuplicates"]):
      tribute["possessions"][type].append(value)
  else:
    tribute["possessions"][type] = [value]

def hasPossession(tribute, type, value):
  if (value == "any"):
    return type in tribute["possessions"] and len(tribute["possessions"][type]) > 0
  else:
    return type in tribute["possessions"] and value in tribute["possessions"][type]

def removePossession(tribute, type, value):
  if (hasPossession(tribute, type, value)):
    tribute["possessions"][type].remove(value)