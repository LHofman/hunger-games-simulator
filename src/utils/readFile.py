import json

def readFile(fileName, type = "text"):
  file = open("settings/%s" % fileName, "r", encoding="utf-8")
  
  if (type == 'json'):
    return json.load(file)

  lines = file.readlines()
  return list(map(lambda line: line.rstrip(), lines))
