import pytest
import vars

from index import readFile, getEvents, readTributes, playGame, printWinner, printRankings

@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch( "random.random", return_value=0 )
  mocker.patch( "random.choice", side_effect=lambda list: list[0] )
  mocker.patch( "random.shuffle" )

startOfGameText = [
  "Tribute 1 from district 1 is still alive",
  "Tribute 2 from district 2 is still alive",
  "The Bloodbath",
  "Tribute 1 flees the cornocopia hastily",
  "Tribute 2 flees the cornocopia hastily",
  "Tribute 1 from district 1 is still alive",
  "Tribute 2 from district 2 is still alive",
  "Day 1",
]

def test_gameWithDeath():
  setUpFullGame("death")
  runGame()

  assertOutput(
    startOfGameText + [
      "Tribute 1 explores the arena.",
      "Tribute 2 dies.",
      "1 cannon shots can be heard in the distance.",
      "Tribute 2 from district 2",
      "The winner is Tribute 1",
      "Final Rankings",
      "2. Tribute 2 from district 2, died during Day 1, has 0 kills",
      "1. Tribute 1 from district 1",
    ]
  )

def test_gameWithKill():
  setUpFullGame("kill")
  runGame()

  assertOutput(
    startOfGameText + [
      "Tribute 2 catches Tribute 1 off guard and kills them.",
      "1 cannon shots can be heard in the distance.",
      "Tribute 1 from district 1",
      "The winner is Tribute 2",
      "Final Rankings",
      "2. Tribute 1 from district 1, died during Day 1, has 0 kills",
      "1. Tribute 2 from district 2",
    ]
  )

def setUpFullGame(testFolder: str):
  vars.gameData = readFile(f"tests/_fullGame/{testFolder}/mockGameData.json", "json")
  vars.events = getEvents()
  vars.tributes = readTributes(f"tests/_fullGame/{testFolder}/mockTributes.txt")
  vars.totalTributes = len(vars.tributes)
  vars.sponsors = readFile(f"tests/_fullGame/{testFolder}/mockSponsors.txt")
  vars.deaths = []
  vars.recentDeaths = []
  vars.outputForTests = []

def runGame():
  playGame()
  printWinner()
  printRankings()
  
def assertOutput(expectedLines):
  for expectedLine in expectedLines:
    assertNextLine(expectedLine)

def assertNextLine(expectedLine):
  actualLine = vars.outputForTests.pop(0)
  actualLine = actualLine.strip('\n\r -')

  while (actualLine == ""):
    actualLine = vars.outputForTests.pop(0)
    actualLine = actualLine.strip('\n\r -')

  assert actualLine == expectedLine
