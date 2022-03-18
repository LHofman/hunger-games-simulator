import vars

def printOutput(message):
  if (vars.gameData["options"]["autoPlay"]):
    outputFile = open("resources/output.txt", "a", encoding="utf-8")
    outputFile.write(f"\n{str(message)}")
    outputFile.close()
  else:
    print(message)