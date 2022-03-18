import vars

def updateTributesData(tribute, type, operation, value):
  if (tribute["name"] not in vars.tributesData):
    vars.tributesData[tribute["name"]] = {}
  
  if (type not in vars.tributesData[tribute["name"]]):
    vars.tributesData[tribute["name"]][type] = value
    return

  if (operation == "add"):
    vars.tributesData[tribute["name"]][type] += value
  elif (operation == "remove"):
    vars.tributesData[tribute["name"]][type] -= value
  else:
    vars.tributesData[tribute["name"]][type] = value