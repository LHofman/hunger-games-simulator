import pytest
from pytest_mock import MockerFixture
from Application.GameExecutor import GameExecutor
from Application.Printers.TestPrinter import TestPrinter
from Domain.types import GameConfig

from index import (
    readFile, # type: ignore
    addNameToEvents,
    readTributes,
    printWinner,
    printRankings,
    GameDataFile
)


@pytest.fixture(autouse=True)
def test_mock(mocker: MockerFixture):
    mocker.patch( 'random.random', return_value=0 )
    mocker.patch( 'random.choice', side_effect=lambda list: list[0] ) # type: ignore
    mocker.patch( 'random.shuffle' )


startOfGameText = [
    'Tribute 1 from district 1 is still alive',
    'Tribute 2 from district 2 is still alive',
    'The Bloodbath',
    'Tribute 1 flees the cornocopia hastily',
    'Tribute 2 flees the cornocopia hastily',
    'Tribute 1 from district 1 is still alive',
    'Tribute 2 from district 2 is still alive',
    'Day 1',
]


def test_gameWithDeath():
    gameConfig: GameConfig = setUpFullGame('death')
    outputArray: list[str] = []

    runGame(gameConfig, outputArray)

    assertOutput(
        outputArray,
        startOfGameText + [
            'Tribute 1 explores the arena.',
            'Tribute 2 dies.',
            '1 cannon shots can be heard in the distance.',
            'Tribute 2 from district 2',
            'The winner is Tribute 1',
            'Final Rankings',
            '2. Tribute 2 from district 2, died during Day 1, has 0 kills',
            '1. Tribute 1 from district 1',
        ]
    )


def test_gameWithKill():
    gameConfig: GameConfig = setUpFullGame('kill')
    outputArray: list[str] = []
    runGame(gameConfig, outputArray)

    assertOutput(
        outputArray,
        startOfGameText + [
            'Tribute 2 catches Tribute 1 off guard and kills them.',
            '1 cannon shots can be heard in the distance.',
            'Tribute 1 from district 1',
            'The winner is Tribute 2',
            'Final Rankings',
            '2. Tribute 1 from district 1, died during Day 1, has 0 kills',
            '1. Tribute 2 from district 2',
        ]
    )


def setUpFullGame(testFolder: str) -> GameConfig:
    gameDataFile: GameDataFile = readFile( # type: ignore
        f'tests/_fullGame/{testFolder}/mockGameData.json', 'json'
    )
    tributes = readTributes(
        gameDataFile['options'],
        f'tests/_fullGame/{testFolder}/mockTributes.txt'
    )
    sponsors: list[str] = readFile( # type: ignore
        f'tests/_fullGame/{testFolder}/mockSponsors.txt'
    )

    return {
        'options': gameDataFile['options'],
        'otherTerms': gameDataFile['replaceTerms'],
        'sponsors': sponsors,
        'totalTributes': len(tributes),
        'allTributes': tributes,
        'events': addNameToEvents(gameDataFile['events']),
        'increaseEventOdds': gameDataFile['increaseEventOdds'],
    }


def runGame(gameConfig: GameConfig, outputArray: list[str]):
    printer = TestPrinter(outputArray)
    gameExecutor = GameExecutor(gameConfig, printer)
    finalGameState = gameExecutor.playGame()
    printWinner(finalGameState, printer)
    printRankings(finalGameState, printer)


def assertOutput(outputArray: list[str], expectedLines: list[str]):
    for expectedLine in expectedLines:
        assertNextLine(outputArray, expectedLine)


def assertNextLine(outputArray: list[str], expectedLine: str):
    actualLine = outputArray.pop(0)
    actualLine = actualLine.strip('\n\r -')

    while (actualLine == ''):
        actualLine = outputArray.pop(0)
        actualLine = actualLine.strip('\n\r -')

    assert actualLine == expectedLine
