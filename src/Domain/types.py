from enum import Enum
from typing import TypedDict, Union
from typing_extensions import NotRequired, Required

class Possession(TypedDict):
    player: Required[int]
    type: Required[str]
    value: Required[str]

class RequiredPossession(Possession):
    inverse: NotRequired[bool]

class GroupSizeType(str, Enum):
    EXACT = 'exact'
    MIN = 'min'
    MAX = 'max'
    
class GroupSize(TypedDict):
    type: Required[GroupSizeType]
    amount: Required[int]
    groupedWith: NotRequired[list[str]]

class UpdateTributeData(TypedDict):
    player: Required[int]
    type: Required[str]
    operation: NotRequired[str]
    value: Required[Union[int, str]]

class Event(TypedDict):
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
    index: int
    name: str
    district: int
    groupedWith: Required[list[str]]
    possessions: Required[dict[str, list[str]]]

class GameOptions(TypedDict):
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
    event: str
    percentage: float

class IncreaseEventOddsMap(TypedDict):
    possessions: dict[str, dict[str, list[IncreaseEventOdds]]]

class GameConfig(TypedDict):
    options: Required[GameOptions]
    otherTerms: Required[dict[str, list[str]]]
    sponsors: Required[list[str]]
    totalTributes: Required[int]
    allTributes: Required[dict[str, Tribute]]
    events: Required[dict[str, Event]]
    increaseEventOdds: Required[IncreaseEventOddsMap]

class GameState(GameConfig):
    eventsOccured: Required[dict[str, int]]
    playersAlive: Required[dict[str, Tribute]]
    deaths: Required[list[list[tuple[str, int]]]]
    recentDeaths: Required[list[tuple[str, int]]]
    tributesData: Required[dict[str, dict[str, Union[int, str]]]]

class GameRoundStateWithoutEvent(GameState):
    time: Required[str]
    exactTime: Required[str]
    currentTribute: Required[Tribute]
    playersRemainingThisRound: Required[dict[str, Tribute]]
    playStandardEvents: Required[bool]

class GameRoundState(GameRoundStateWithoutEvent):
    event: Required[Event]
    