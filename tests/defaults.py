from domain.types import (
    Event,
    GameOptions,
    GameRoundState,
    GameRoundStateWithoutEvent,
    Tribute,
)

default_event: Event = {
    'name': 'Event Name',
    'text': 'Event Text',
}
default_tribute: Tribute = {
    'index': 1,
    'name': 'Player1',
    'district': 1,
    'grouped_with': [],
    'possessions': {},
}
default_game_options: GameOptions = {
    'betray_teammates': False,
    'speed': 1,
    'district_can_win_together': False,
    'auto_play': False,
    'show_fallen_tributes': False,
    'possessions_without_duplicates': [],
    'districts': 0,
    'players_per_district': 0,
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
    'increase_event_odds': { 'possessions': {} },
    'events_occured': {},
    'players_alive': {},
    'deaths': [],
    'recent_deaths': [],
    'tributes_data': {},
    'time': '',
    'exact_time': '',
    'current_tribute': default_tribute,
    'players_remaining_this_round': {},
    'play_standard_events': True,
}
default_game_round_state: GameRoundState = {
    **default_game_round_state_without_event,
    'event': default_event,
}