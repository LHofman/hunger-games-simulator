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
    groupedWith: NotRequired[list[str]]


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
    maxOccurances: NotRequired[int]
    percentage: NotRequired[float]
    players: NotRequired[int]
    deaths: NotRequired[list[str]]
    requiresPossessions: NotRequired[list[RequiredPossession]]
    time: NotRequired[Union[str, list[str]]]
    requireGroupSize: NotRequired[GroupSize]
    killTeammates: NotRequired[bool]
    formGroup: NotRequired[list[str]]
    splitGroup: NotRequired[list[str]]
    deaths: NotRequired[list[str]]
    updateTributesData: NotRequired[list[UpdateTributeData]]
    addPossessions: NotRequired[list[Possession]]
    removePossessions: NotRequired[list[Possession]]


class Tribute(TypedDict):
    """Represent a tribute (player) in the game."""

    index: int
    name: str
    district: int
    groupedWith: Required[list[str]]
    possessions: Required[dict[str, list[str]]]


class GameOptions(TypedDict):
    """Represent the configuration options for the game."""

    betrayTeammates: bool
    speed: int
    districtCanWinTogether: bool
    autoPlay: bool
    showFallenTributes: bool
    possessionsWithoutDuplicates: list[str]
    districts: int
    playersPerDistrict: int
    districtsAreTeammates: bool
    oneSponsorPerTribute: bool


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
    otherTerms: Required[dict[str, list[str]]]
    sponsors: Required[list[str]]
    totalTributes: Required[int]
    allTributes: Required[dict[str, Tribute]]
    events: Required[dict[str, Event]]
    increaseEventOdds: Required[IncreaseEventOddsMap]


class GameState(GameConfig):
    """Represent the current state of the game."""

    eventsOccured: Required[dict[str, int]]
    playersAlive: Required[dict[str, Tribute]]
    deaths: Required[list[list[tuple[str, int]]]]
    recentDeaths: Required[list[tuple[str, int]]]
    tributesData: Required[dict[str, dict[str, Union[int, str]]]]


class GameRoundStateWithoutEvent(GameState):
    """Represent the state of the game during a round, without the current event."""

    time: Required[str]
    exactTime: Required[str]
    currentTribute: Required[Tribute]
    playersRemainingThisRound: Required[dict[str, Tribute]]
    playStandardEvents: Required[bool]


class GameRoundState(GameRoundStateWithoutEvent):
    """Represent the state of the game during a round, including the current event."""

    event: Required[Event]
    