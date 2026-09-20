"""Game executor for the Hunger Games simulator."""

import random
import sys

from Application.EventPicker import EventPicker
from Application.handleEventEffects import handleEventEffects
from Application.Printer import Printer
from Application.replaceTextTerms import replaceTextTerms
from Domain.EventRules.Possessions import Possessions
from Domain.types import (
    GameConfig,
    GameRoundState,
    GameRoundStateWithoutEvent,
    GameState,
    Tribute,
)


class GameExecutor:
    """Execute the game based on the given configuration and prints the results."""

    gameState: GameState

    def __init__(self, gameConfig: GameConfig, printer: Printer):
        """Initialize the GameExecutor with the given game configuration and printer."""
        self.gameState = {
            **gameConfig,
            'eventsOccured': {},
            'playersAlive': gameConfig['allTributes'].copy(),
            'deaths': [],
            'recentDeaths': [],
            'tributesData': {},
        }
        self.printer = printer

    def playGame(self) -> GameState:
        """Play the game until there is a winner and returns the final game state."""
        self._playRound('The Bloodbath', 'bloodbath', False)
        day = 0
        while (not self._isGameOver()):
            day += 1
            self._playRound(f'Day {day}', 'day', True)
            self._showFallenTributes()
            self._playRound(f'Night {day}', 'night', True)
            if day == 5: self._playRound('The Feast', 'feast', False)

        return self.gameState

    def _playRound(
        self,
        text: str,
        time: str,
        playStandardEvents: bool,
    ) -> None:
        if self._isGameOver(): return

        self._shuffleTributes()
        self._readInput()
        self.printer.print(text)
        self._playList(time, text, playStandardEvents)
        self.printer.print('\n---')

    def _playList(
        self,
        time: str,
        text: str,
        playStandardEvents: bool,
    ) -> None:
        tributesLeft = self.gameState['playersAlive'].copy()
        played = 0
        total = amountLeft = len(tributesLeft)
        while (amountLeft > 0 and len(self.gameState['playersAlive']) > 1):
            self._checkEveryoneInTheSameGroup()

            tribute = list(tributesLeft.values())[0]
            del tributesLeft[tribute['name']]
            percentage = self._percentageOfPlaying(total, time)
            rnd = random.random()
            if rnd < percentage:
                self._playTribute(
                    time,
                    text,
                    playStandardEvents,
                    tribute,
                    tributesLeft,
                )
                played += 1
                
            amountLeft = len(tributesLeft)

        if played == 0:
            self._playList(time, text, playStandardEvents)

    def _playTribute(
        self,
        time: str,
        text: str,
        playStandardEvents: bool,
        tribute: Tribute,
        tributesLeft: dict[str, Tribute],
    ) -> None:
        gameRoundStateWithoutEvent: GameRoundStateWithoutEvent = {
            **self.gameState,
            'time': time,
            'exactTime': text,
            'playStandardEvents': playStandardEvents,
            'currentTribute': tribute,
            'playersRemainingThisRound': tributesLeft,
        }

        event = EventPicker().getEvent(gameRoundStateWithoutEvent)

        gameRoundState: GameRoundState = {
            **gameRoundStateWithoutEvent,
            'event': event,
        }

        textAndTerms = replaceTextTerms(gameRoundState)
        
        handleEventEffects(gameRoundState, textAndTerms)
        
        self.gameState.update({k: gameRoundState[k] for k in self.gameState}) # type: ignore

        self.printer.print(textAndTerms['text'])

    def _showFallenTributes(self) -> None:
        if (
            len(self.gameState['recentDeaths']) > 0
            and self.gameState['options']['showFallenTributes']
        ):
            if not self._isGameOver(): self._readInput()
            self.printer.print(
                f'{len(self.gameState["recentDeaths"])} cannon shots '
                'can be heard in the distance.',
            )
            for playerName, district in self.gameState['recentDeaths']:
                self.printer.print(f'{playerName} from district {district}')
            self.printer.print('---')

        self.gameState['deaths'].append(self.gameState['recentDeaths'].copy())
        self.gameState['recentDeaths'].clear()

    def _isGameOver(self) -> bool:
        if len(self.gameState['playersAlive']) <= 1: return True

        if self.gameState['options']['districtCanWinTogether']:
            isEveryoneInSameDistrict = True
            for name, tribute in self.gameState['playersAlive'].items():
                for name2, tribute2 in self.gameState['playersAlive'].items():
                    if (
                        name2 != name
                        and tribute2['district'] != tribute['district']
                    ):
                        isEveryoneInSameDistrict = False
                        break
                if not isEveryoneInSameDistrict: break
        
            if isEveryoneInSameDistrict: return True

        return False

    def _shuffleTributes(self) -> None:
        l = list(self.gameState['playersAlive'].items())
        random.shuffle(l)
        self.gameState['playersAlive'] = dict(l)

    def _readInput(self) -> None:
        if self.gameState['options']['autoPlay']:
            self.printer.print('')
            self._printStatus()
            return

        userInput = input(
            'Press Enter to continue, '
            'or type status to see the current status of all tributes: ',
        )
        self.printer.print('')

        if userInput == 'stop': sys.exit()

        if userInput == 'status':
            self._printStatus()
            self._readInput()

    def _printStatus(self) -> None:
        for (name, tribute) in sorted(self.gameState['playersAlive'].items()):
            possessions = ''
            for (type, values) in tribute['possessions'].items():
                if Possessions.doesTributeHavePossession(tribute, type, 'any'):
                    possessions = f'{possessions}{type}: {", ".join(values)}, '

            if possessions:
                possessions = f', has {possessions[0: -2]}'

            self.printer.print(
                f'{name} from district {tribute["district"]} '
                f'is still alive{possessions}',
            )

        self.printer.print('\n---')

    def _checkEveryoneInTheSameGroup(self) -> None:
        for name, tribute in self.gameState['playersAlive'].items():
            for name2 in self.gameState['playersAlive'].keys():
                if name2 != name and name2 not in tribute['groupedWith']:
                    return

        for name, _ in self.gameState['playersAlive'].items():
            self.gameState['playersAlive'][name]['groupedWith'].clear()

        self.printer.print(
            'The remaining tributes realize they '
            'are the only ones left and split up',
        )

    def _percentageOfPlaying(self, total: int, time: str) -> float:
        if time in ['bloodbath', 'feast']: return 1
        
        if total > 25: return 15/total
        if total > 15: return 0.5
        if total > 5: return 0.75
        return 1
