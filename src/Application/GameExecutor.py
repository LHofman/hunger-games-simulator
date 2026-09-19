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
    gameState: GameState

    def __init__(self, gameConfig: GameConfig, printer: Printer):
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
        self.__playRound('The Bloodbath', 'bloodbath', False)
        day = 0
        while (not self.__isGameOver()):
            day += 1
            self.__playRound(f'Day {day}', 'day', True)
            self.__showFallenTributes()
            self.__playRound(f'Night {day}', 'night', True)
            if day == 5: self.__playRound('The Feast', 'feast', False)

        return self.gameState

    def __playRound(
        self,
        text: str,
        time: str,
        playStandardEvents: bool,
    ) -> None:
        if self.__isGameOver(): return

        self.__shuffleTributes()
        self.__readInput()
        self.printer.print(text)
        self.__playList(time, text, playStandardEvents)
        self.printer.print('\n---')

    def __playList(
        self,
        time: str,
        text: str,
        playStandardEvents: bool,
    ) -> None:
        tributesLeft = self.gameState['playersAlive'].copy()
        played = 0
        total = amountLeft = len(tributesLeft)
        while (amountLeft > 0 and len(self.gameState['playersAlive']) > 1):
            self.__checkEveryoneInTheSameGroup()

            tribute = list(tributesLeft.values())[0]
            del tributesLeft[tribute['name']]
            percentage = self.__percentageOfPlaying(total, time)
            rnd = random.random()
            if rnd < percentage:
                self.__playTribute(
                    time,
                    text,
                    playStandardEvents,
                    tribute,
                    tributesLeft,
                )
                played += 1
                
            amountLeft = len(tributesLeft)

        if played == 0:
            self.__playList(time, text, playStandardEvents)

    def __playTribute(
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

    def __showFallenTributes(self) -> None:
        if (
            len(self.gameState['recentDeaths']) > 0
            and self.gameState['options']['showFallenTributes']
        ):
            if not self.__isGameOver(): self.__readInput()
            self.printer.print(
                f'{len(self.gameState["recentDeaths"])} cannon shots '
                'can be heard in the distance.',
            )
            for playerName, district in self.gameState['recentDeaths']:
                self.printer.print(f'{playerName} from district {district}')
            self.printer.print('---')

        self.gameState['deaths'].append(self.gameState['recentDeaths'].copy())
        self.gameState['recentDeaths'].clear()

    def __isGameOver(self) -> bool:
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

    def __shuffleTributes(self) -> None:
        l = list(self.gameState['playersAlive'].items())
        random.shuffle(l)
        self.gameState['playersAlive'] = dict(l)

    def __readInput(self) -> None:
        if self.gameState['options']['autoPlay']:
            self.printer.print('')
            self.__printStatus()
            return

        userInput = input(
            'Press Enter to continue, '
            'or type status to see the current status of all tributes: ',
        )
        self.printer.print('')

        if userInput == 'stop': sys.exit()

        if userInput == 'status':
            self.__printStatus()
            self.__readInput()

    def __printStatus(self) -> None:
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

    def __checkEveryoneInTheSameGroup(self) -> None:
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

    def __percentageOfPlaying(self, total: int, time: str) -> float:
        if time in ['bloodbath', 'feast']: return 1
        
        if total > 25: return 15/total
        if total > 15: return 0.5
        if total > 5: return 0.75
        return 1
