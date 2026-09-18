import vars

def printOutput(message):
  if ("collectOutputForTests" in vars.gameData["options"] and vars.gameData["options"]["collectOutputForTests"]):
    vars.outputForTests.append(message)
  elif (vars.gameData["options"]["autoPlay"]):
    outputFile = open("resources/output.txt", "a", encoding="utf-8")
    outputFile.write(f"\n{str(message)}")
    outputFile.close()
  else:
    print(message)