import pytest

from pytest_mock import MockerFixture

from application.game_executor import GameExecutor
from application.printers.test_printer import TestPrinter
from domain.types import GameConfig

from index import (
    read_file,  # type: ignore
    read_game_data_file,
    add_name_to_events,
    read_tributes,
    print_winner,
    print_rankings,
    GameDataFile,
)


@pytest.fixture(autouse = True)
def test_mock(mocker: MockerFixture):
    mocker.patch('random.random', return_value=0)
    mocker.patch('random.choice', side_effect=lambda list: list[0]) # type: ignore
    mocker.patch('random.shuffle')


start_of_game_text = [
    'Tribute 1 from district 1 is still alive',
    'Tribute 2 from district 2 is still alive',
    'The Bloodbath',
    'Tribute 1 flees the cornocopia hastily',
    'Tribute 2 flees the cornocopia hastily',
    'Tribute 1 from district 1 is still alive',
    'Tribute 2 from district 2 is still alive',
    'Day 1',
]


def test_game_with_death():
    game_config: GameConfig = set_up_full_game('death')
    output_array: list[str] = []

    run_game(game_config, output_array)

    assert_output(
        output_array,
        start_of_game_text + [
            'Tribute 1 explores the arena.',
            'Tribute 2 dies.',
            '1 cannon shots can be heard in the distance.',
            'Tribute 2 from district 2',
            'The winner is Tribute 1',
            'Final Rankings',
            '2. Tribute 2 from district 2, died during Day 1, has 0 kills',
            '1. Tribute 1 from district 1',
        ],
    )


def test_game_with_kill():
    game_config: GameConfig = set_up_full_game('kill')
    output_array: list[str] = []
    run_game(game_config, output_array)

    assert_output(
        output_array,
        start_of_game_text + [
            'Tribute 2 catches Tribute 1 off guard and kills them.',
            '1 cannon shots can be heard in the distance.',
            'Tribute 1 from district 1',
            'The winner is Tribute 2',
            'Final Rankings',
            '2. Tribute 1 from district 1, died during Day 1, has 0 kills',
            '1. Tribute 2 from district 2',
        ],
    )


def set_up_full_game(test_folder: str) -> GameConfig:
    game_data_file: GameDataFile = read_game_data_file( # type: ignore
        f'tests/_full_game/{test_folder}/mock_game_data.json',
    )
    tributes = read_tributes(
        game_data_file['options'],
        f'tests/_full_game/{test_folder}/mock_tributes.txt',
    )
    sponsors: list[str] = read_file( # type: ignore
        f'tests/_full_game/{test_folder}/mock_sponsors.txt',
    )

    return {
        'options': game_data_file['options'],
        'other_terms': game_data_file['replace_terms'],
        'sponsors': sponsors,
        'total_tributes': len(tributes),
        'all_tributes': tributes,
        'events': add_name_to_events(game_data_file['events']),
        'increase_event_odds': game_data_file['increase_event_odds'],
    }


def run_game(game_config: GameConfig, output_array: list[str]):
    printer = TestPrinter(output_array)
    game_executor = GameExecutor(game_config, printer)
    final_game_state = game_executor.play_game()
    print_winner(final_game_state, printer)
    print_rankings(final_game_state, printer)


def assert_output(output_array: list[str], expected_lines: list[str]):
    for expected_line in expected_lines:
        assert_next_line(output_array, expected_line)


def assert_next_line(output_array: list[str], expected_line: str):
    actual_line = output_array.pop(0)
    actual_line = actual_line.strip('\n\r -')

    while (actual_line == ''):
        actual_line = output_array.pop(0)
        actual_line = actual_line.strip('\n\r -')

    assert actual_line == expected_line
