from domain.tribute import Tribute
from domain.types import (
    Event,
    GameOptions,
    GameRoundState,
    GameRoundStateWithoutEvent,
)

default_event: Event = {
    'name': 'Event Name',
    'text': 'Event Text',
}
default_tribute: Tribute = Tribute(1, 'Tribute1', 1)
default_game_options: GameOptions = {
    'betray_teammates': False,
    'speed': 1,
    'district_can_win_together': False,
    'auto_play': False,
    'show_fallen_tributes': False,
    'possessions_without_duplicates': [],
    'districts': 0,
    'tributes_per_district': 0,
    'districts_are_teammates': False,
    'one_sponsor_per_tribute': False,
}
default_game_round_state_without_event: GameRoundStateWithoutEvent = {
    'options': default_game_options,
    'other_terms': {},
    'sponsors': [],
    'total_tributes': 0,
    'all_tributes': {},
    'events': {},
    'increase_event_odds': {'possessions': {}},
    'events_occured': {},
    'tributes_alive': {},
    'deaths': [],
    'recent_deaths': [],
    'time': '',
    'exact_time': '',
    'current_tribute': default_tribute,
    'tributes_remaining_this_round': {},
    'play_standard_events': True,
}
default_game_round_state: GameRoundState = {
    **default_game_round_state_without_event,
    'event': default_event,
}
