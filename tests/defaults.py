from Domain.types import Event, GameOptions, GameRoundState, GameRoundStateWithoutEvent, Tribute

defaultEvent: Event = {
  'name': 'Event Name',
  'text': 'Event Text',
}
defaultTribute: Tribute = {
  'index': 1,
  'name': 'Player1',
  'district': 1,
  'groupedWith': [],
  'possessions': {},
}
defaultGameOptions: GameOptions = {
  'betrayTeammates': False,
  'speed': 1,
  'districtCanWinTogether': False,
  'autoPlay': False,
  'showFallenTributes': False,
  'possessionsWithoutDuplicates': [],
  'districts': 0,
  'playersPerDistrict': 0,
  'districtsAreTeammates': False,
  'oneSponsorPerTribute': False,
}
defaultGameRoundStateWithoutEvent: GameRoundStateWithoutEvent = {
  'options': defaultGameOptions,
  'otherTerms': {},
  'sponsors': [],
  'totalTributes': 0,
  'allTributes': {},
  'events': {},
  'increaseEventOdds': { 'possessions': {} },
  'eventsOccured': {},
  'playersAlive': {},
  'deaths': [],
  'recentDeaths': [],
  'tributesData': {},
  'time': '',
  'exactTime': '',
  'currentTribute': defaultTribute,
  'playersRemainingThisRound': {},
  'playStandardEvents': True,
}
defaultGameRoundState: GameRoundState = {
  **defaultGameRoundStateWithoutEvent,
  'event': defaultEvent,
}