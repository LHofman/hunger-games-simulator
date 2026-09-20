"""Game executor for the Hunger Games simulator."""

import random
import sys

from application.event_picker import EventPicker
from application.handle_event_effects import handle_event_effects
from application.printer import Printer
from application.replace_text_terms import replace_text_terms
from domain.event_rules.possessions import Possessions
from domain.types import (
    GameConfig,
    GameRoundState,
    GameRoundStateWithoutEvent,
    GameState,
    Tribute,
)


class GameExecutor:
    """Execute the game based on the given configuration and prints the results."""

    _game_state: GameState

    def __init__(self, game_config: GameConfig, printer: Printer):
        """Initialize the GameExecutor with the given game configuration and printer."""
        self._game_state = {
            **game_config,
            'events_occured': {},
            'tributes_alive': game_config['all_tributes'].copy(),
            'deaths': [],
            'recent_deaths': [],
            'tributes_data': {},
        }
        self.printer = printer

    def play_game(self) -> GameState:
        """Play the game until there is a winner and returns the final game state."""
        self._play_round('The Bloodbath', 'bloodbath', False)
        day = 0
        while not self._is_game_over():
            day += 1
            self._play_round(f'Day {day}', 'day', True)
            self._show_fallen_tributes()
            self._play_round(f'Night {day}', 'night', True)
            if day == 5:
                self._play_round('The Feast', 'feast', False)

        return self._game_state

    def _play_round(
        self,
        text: str,
        time: str,
        play_standard_events: bool,
    ) -> None:
        if self._is_game_over():
            return

        self._shuffle_tributes()
        self._read_input()
        self.printer.print(text)
        self._playList(time, text, play_standard_events)
        self.printer.print('\n---')

    def _playList(
        self,
        time: str,
        text: str,
        play_standard_events: bool,
    ) -> None:
        tributes_left = self._game_state['tributes_alive'].copy()
        played = 0
        total = amount_left = len(tributes_left)
        while amount_left > 0 and len(self._game_state['tributes_alive']) > 1:
            self._check_everyone_in_the_same_group()

            tribute = next(iter(tributes_left.values()))
            del tributes_left[tribute['name']]
            percentage = self._percentage_of_playing(total, time)
            rnd = random.random()
            if rnd < percentage:
                self._playTribute(
                    time,
                    text,
                    play_standard_events,
                    tribute,
                    tributes_left,
                )
                played += 1

            amount_left = len(tributes_left)

        if played == 0:
            self._playList(time, text, play_standard_events)

    def _playTribute(
        self,
        time: str,
        text: str,
        play_standard_events: bool,
        tribute: Tribute,
        tributes_left: dict[str, Tribute],
    ) -> None:
        game_round_state_without_event: GameRoundStateWithoutEvent = {
            **self._game_state,
            'time': time,
            'exact_time': text,
            'play_standard_events': play_standard_events,
            'current_tribute': tribute,
            'tributes_remaining_this_round': tributes_left,
        }

        event = EventPicker().get_event(game_round_state_without_event)

        game_round_state: GameRoundState = {
            **game_round_state_without_event,
            'event': event,
        }

        text_and_terms = replace_text_terms(game_round_state)

        handle_event_effects(game_round_state, text_and_terms)

        self._game_state.update(
            {k: game_round_state[k] for k in self._game_state},  # type: ignore
        )

        self.printer.print(text_and_terms['text'])

    def _show_fallen_tributes(self) -> None:
        if (
            self._game_state['recent_deaths']
            and self._game_state['options']['show_fallen_tributes']
        ):
            if not self._is_game_over():
                self._read_input()
            self.printer.print(
                f'{len(self._game_state["recent_deaths"])} cannon shots '
                'can be heard in the distance.',
            )
            for tribute_name, district in self._game_state['recent_deaths']:
                self.printer.print(f'{tribute_name} from district {district}')
            self.printer.print('---')

        self._game_state['deaths'].append(
            self._game_state['recent_deaths'].copy()
        )
        self._game_state['recent_deaths'].clear()

    def _is_game_over(self) -> bool:
        if len(self._game_state['tributes_alive']) <= 1:
            return True

        if self._game_state['options']['district_can_win_together']:
            is_everyone_in_same_district = True
            for name, tribute in self._game_state['tributes_alive'].items():
                for name2, tribute2 in self._game_state[
                    'tributes_alive'
                ].items():
                    if (
                        name2 != name
                        and tribute2['district'] != tribute['district']
                    ):
                        is_everyone_in_same_district = False
                        break

                if not is_everyone_in_same_district:
                    break

            if is_everyone_in_same_district:
                return True

        return False

    def _shuffle_tributes(self) -> None:
        l = list(self._game_state['tributes_alive'].items())
        random.shuffle(l)
        self._game_state['tributes_alive'] = dict(l)

    def _read_input(self) -> None:
        if self._game_state['options']['auto_play']:
            self.printer.print('')
            self._print_status()
            return

        user_input = input(
            'Press Enter to continue, '
            'or type status to see the current status of all tributes: ',
        )
        self.printer.print('')

        if user_input == 'stop':
            sys.exit()

        if user_input == 'status':
            self._print_status()
            self._read_input()

    def _print_status(self) -> None:
        for name, tribute in sorted(self._game_state['tributes_alive'].items()):
            possessions = ''
            for type, values in tribute['possessions'].items():
                if Possessions.does_tribute_have_possession(
                    tribute,
                    type,
                    'any',
                ):
                    possessions = f'{possessions}{type}: {", ".join(values)}, '

            if possessions:
                possessions = f', has {possessions[0:-2]}'

            self.printer.print(
                f'{name} from district {tribute["district"]} '
                f'is still alive{possessions}',
            )

        self.printer.print('\n---')

    def _check_everyone_in_the_same_group(self) -> None:
        for name, tribute in self._game_state['tributes_alive'].items():
            for name2 in self._game_state['tributes_alive']:
                if name2 != name and name2 not in tribute['grouped_with']:
                    return

        for name in self._game_state['tributes_alive']:
            self._game_state['tributes_alive'][name]['grouped_with'].clear()

        self.printer.print(
            'The remaining tributes realize they '
            'are the only ones left and split up',
        )

    def _percentage_of_playing(self, total: int, time: str) -> float:
        if time in ['bloodbath', 'feast']:
            return 1

        if total > 25:
            return 15 / total
        if total > 15:
            return 0.5
        if total > 5:
            return 0.75
        return 1
