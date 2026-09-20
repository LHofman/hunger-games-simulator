"""Types used in the hunger games simulator."""

from enum import Enum
from typing import TypedDict, Union
from typing_extensions import NotRequired, Required


class Possession(TypedDict):
    """Represent a possession that a tribute can have."""

    player: Required[int]
    type: Required[str]
    value: Required[str]


class RequiredPossession(Possession):
    """Represent a required possession that a tribute must have."""

    inverse: NotRequired[bool]


class GroupSizeType(str, Enum):
    """Represent the type of group size requirement for an event."""

    EXACT = 'exact'
    MIN = 'min'
    MAX = 'max'


class GroupSize(TypedDict):
    """Represent a group size requirement for an event."""

    type: Required[GroupSizeType]
    amount: Required[int]
    grouped_with: NotRequired[list[str]]


class UpdateTributeData(TypedDict):
    """Represent an update to a tribute's data that can be applied by an event."""

    player: Required[int]
    type: Required[str]
    operation: NotRequired[str]
    value: Required[Union[int, str]]


class Event(TypedDict):
    """Represent an event that can occur in the game."""

    name: Required[str]
    text: Required[str]
    ignore: NotRequired[bool]
    max_occurances: NotRequired[int]
    percentage: NotRequired[float]
    players: NotRequired[int]
    deaths: NotRequired[list[str]]
    requires_possessions: NotRequired[list[RequiredPossession]]
    time: NotRequired[Union[str, list[str]]]
    require_group_size: NotRequired[GroupSize]
    kill_teammates: NotRequired[bool]
    form_group: NotRequired[list[str]]
    split_group: NotRequired[list[str]]
    update_tributes_data: NotRequired[list[UpdateTributeData]]
    add_possessions: NotRequired[list[Possession]]
    remove_possessions: NotRequired[list[Possession]]


class Tribute(TypedDict):
    """Represent a tribute (player) in the game."""

    index: int
    name: str
    district: int
    grouped_with: Required[list[str]]
    possessions: Required[dict[str, list[str]]]


class GameOptions(TypedDict):
    """Represent the configuration options for the game."""

    betray_teammates: bool
    speed: int
    district_can_win_together: bool
    auto_play: bool
    show_fallen_tributes: bool
    possessions_without_duplicates: list[str]
    districts: int
    players_per_district: int
    districts_are_teammates: bool
    one_sponsor_per_tribute: bool


class IncreaseEventOdds(TypedDict):
    """Represent an increase in the odds of an event occurring."""

    event: str
    percentage: float


class IncreaseEventOddsMap(TypedDict):
    """Represent a mapping of possessions to events and their increased odds."""

    possessions: dict[str, dict[str, list[IncreaseEventOdds]]]


class GameConfig(TypedDict):
    """Represent the configuration of the game."""

    options: Required[GameOptions]
    other_terms: Required[dict[str, list[str]]]
    sponsors: Required[list[str]]
    total_tributes: Required[int]
    all_tributes: Required[dict[str, Tribute]]
    events: Required[dict[str, Event]]
    increase_event_odds: Required[IncreaseEventOddsMap]


class GameState(GameConfig):
    """Represent the current state of the game."""

    events_occured: Required[dict[str, int]]
    players_alive: Required[dict[str, Tribute]]
    deaths: Required[list[list[tuple[str, int]]]]
    recent_deaths: Required[list[tuple[str, int]]]
    tributes_data: Required[dict[str, dict[str, Union[int, str]]]]


class GameRoundStateWithoutEvent(GameState):
    """Represent the state of the game during a round, without the current event."""

    time: Required[str]
    exact_time: Required[str]
    current_tribute: Required[Tribute]
    players_remaining_this_round: Required[dict[str, Tribute]]
    play_standard_events: Required[bool]


class GameRoundState(GameRoundStateWithoutEvent):
    """Represent the state of the game during a round, including the current event."""

    event: Required[Event]
    