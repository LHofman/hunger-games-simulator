"""Main entry point for the Hunger Games simulator."""

from __future__ import annotations

import json
import re
from typing import TypedDict

from application.game_executor import GameExecutor
from domain.printer import Printer
from application.printers.file_printer import FilePrinter
from domain.tribute import Tribute
from domain.types import (
    Event,
    GameConfig,
    GameOptions,
    GameState,
    IncreaseEventOddsMap,
)

printer: Printer = Printer()


def to_snake_case(text: str) -> str:
    """Convert a string from camelCase to snake_case."""
    s1 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text)
    return re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s1).lower()


def camel_to_snake_dict(d: dict) -> dict:  # type: ignore
    """Converts top-level dictionary keys to snake_case."""
    return {to_snake_case(k): v for k, v in d.items()}  # type: ignore


def read_file(file_name: str, type: str = 'text') -> dict | list | None:  # type: ignore
    """Read a file and returns its contents as a dictionary (for JSON) or a list of lines (for text)."""
    with open(file_name, 'r', encoding='utf-8') as file:
        if type == 'json':
            return json.load(file)

        lines = file.readlines()
        return [line.rstrip() for line in lines]  # type: ignore


class GameDataFile(TypedDict):
    """Represent the structure of the game data file."""

    options: GameOptions
    increase_event_odds: IncreaseEventOddsMap
    events: dict[str, Event]
    replace_terms: dict[str, list[str]]


def read_game_data_file(file_name: str) -> GameDataFile:
    """Read the game data file and returns its contents as a GameDataFile object."""
    raw_game_data_file = read_file(file_name, 'json')  # type: ignore

    formatted_events: dict[str, Event] = {  # type: ignore
        event_name: camel_to_snake_dict(event)  # type: ignore
        for event_name, event in raw_game_data_file['events'].items()  # type: ignore
    }

    return {
        'options': camel_to_snake_dict(raw_game_data_file['options']),  # type: ignore
        'increase_event_odds': camel_to_snake_dict(
            raw_game_data_file['increaseEventOdds'],  # type: ignore
        ),
        'events': formatted_events,
        'replace_terms': raw_game_data_file['replaceTerms'],  # type: ignore
    }


def read_tributes(
    game_options: GameOptions,
    tributes_file_name: str,
) -> dict[str, Tribute]:
    """Read the tributes from a file and returns a dictionary of Tribute objects."""
    with open(tributes_file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if game_options['districts'] > 0:
        tributes_per_district = len(lines) / game_options['districts']
    elif game_options['tributes_per_district'] > 0:
        tributes_per_district = game_options['tributes_per_district']
    else:
        tributes_per_district = 0

    tributes: dict[str, Tribute] = {}
    for ao_tributes, line in enumerate(lines, start=1):
        name = line.rstrip()
        tributes[name] = Tribute(
            ao_tributes,
            name,
            (
                int(((ao_tributes - 1) / tributes_per_district) + 1)
                if tributes_per_district > 0
                else 0
            ),
        )

    if game_options['districts_are_teammates']:
        for name, tribute in list(tributes.items()):
            for name2, tribute2 in list(tributes.items()):
                if name2 != name and tribute2.district == tribute.district:
                    tribute.group_with(name2)

    return tributes


def add_name_to_events(events: dict[str, Event]) -> dict[str, Event]:
    """Add the name of each event to its corresponding Event object."""
    for name, event in events.items():
        event['name'] = name
        events[name] = event

    return events


def print_winner(game_state: GameState, printer: Printer):
    """Print the winner(s) of the game."""
    winners = list(game_state['tributes_alive'].keys())
    if len(winners) == 1:
        printer.print(f'The winner is {winners[0]}')
    elif len(winners) > 1:
        printer.print(f'The winners are {", ".join(winners)}')
    else:
        printer.print('There are no winners today')


def print_rankings(game_state: GameState, printer: Printer):
    """Print the final rankings of the tributes."""
    printer.print('\n\n\n---\nFinal Rankings')

    for tribute_deaths in game_state['deaths']:
        for tribute, district in tribute_deaths:
            tribute_data = game_state['tributes_data'][tribute]
            printer.print(
                f'{game_state["total_tributes"]}. '
                f'{tribute} from district {district}, '
                f'died during {tribute_data["time of death"]}, '
                f'has {tribute_data.get("kills", 0)} kills',
            )
            game_state['total_tributes'] -= 1

    for name, tribute in list(game_state['tributes_alive'].items()):
        printer.print(f'1. {name} from district {tribute.district}')


if __name__ == '__main__':
    game_data_file: GameDataFile = read_game_data_file(
        'settings/game_data.json'
    )

    if game_data_file['options']['auto_play']:
        printer = FilePrinter('resources/output.txt')

    tributes = read_tributes(
        game_data_file['options'],
        'settings/tributes.txt',
    )
    sponsors: list[str] = read_file('settings/sponsors.txt')  # type: ignore

    if game_data_file['options']['auto_play']:
        with open('resources/output.txt', 'w') as output_file:
            output_file.write('')

    printer.print('-' * 114)

    game_state: GameConfig = {
        'options': game_data_file['options'],
        'other_terms': game_data_file['replace_terms'],
        'sponsors': sponsors,
        'total_tributes': len(tributes),
        'all_tributes': tributes,
        'events': add_name_to_events(game_data_file['events']),
        'increase_event_odds': game_data_file['increase_event_odds'],
    }

    game_executor = GameExecutor(game_state, printer)
    final_game_state = game_executor.play_game()

    print_winner(final_game_state, printer)
    print_rankings(final_game_state, printer)
