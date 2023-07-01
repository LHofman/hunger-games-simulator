import json

class FileReader:

  def read(self, fileName: str, type: str = "text"):
    file = open("settings/%s" % fileName, "r", encoding="utf-8")
    
    if (type == 'json'):
      return json.load(file)

    lines = file.readlines()
    return list(map(lambda line: line.rstrip(), lines))
