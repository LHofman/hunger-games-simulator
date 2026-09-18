import pytest
import vars
from canPlayEvent import canPlayEvent

# Mock tribute possessions, alsways has "Test Item 1" and "Test Item 2"
@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object(
    vars,
    "tributes",
    [ "Player1", "Player2", "Player3" ]
  )
  mocker.patch( "canPlayEvent.checkHasRequiredPossessions", return_value=True )
  mocker.patch( "canPlayEvent.checkCanPlayTimedEvents", return_value=True )
  mocker.patch( "canPlayEvent.checkCompliesWithRequiredGroupSize", return_value=True )
  mocker.patch( "canPlayEvent.checkCanBetrayTeammates", return_value=True )

providers = [
  ({
    "id": "A standard event can be played.",
    "event": {},
    "tribute": {},
    "playersRemaining": {},
    "time": "day",
    "playStandardEvents": True,
    "expectedCanPlayEvent": True,
  }),
  ({
    "id": "An event that is ignored cannot be played.",
    "event": { "ignore": True },
    "tribute": {},
    "playersRemaining": {},
    "time": "day",
    "playStandardEvents": True,
    "expectedCanPlayEvent": False,
  }),
  ({
    "id": "An event that requires 1 player can be played by the current tribute",
    "event": { "players": 1},
    "tribute": {},
    "playersRemaining": {},
    "time": "day",
    "playStandardEvents": True,
    "expectedCanPlayEvent": True,
  }),
  ({
    "id": "An event that requires 2 players can be played by if there is 1 other player remaining",
    "event": { "players": 2},
    "tribute": {},
    "playersRemaining": { "Player2": {} },
    "time": "day",
    "playStandardEvents": True,
    "expectedCanPlayEvent": True,
  }),
  ({
    "id": "An event that requires 2 players cannot be played if there are no other players remaining",
    "event": { "players": 2},
    "tribute": {},
    "playersRemaining": {},
    "time": "day",
    "playStandardEvents": True,
    "expectedCanPlayEvent": False,
  }),
  ({
    "id": "An event that forms a group can be played if there are more than 2 tributes alive",
    "event": { "formGroup": True },
    "tribute": {},
    "playersRemaining": {},
    "time": "day",
    "playStandardEvents": True,
    "expectedCanPlayEvent": True,
  }),
]

@pytest.mark.parametrize("provider", providers, ids=lambda p: f"{p['id']}")
def test_canPlayEvent(provider):
  result = canPlayEvent(
    provider["tribute"],
    provider["playersRemaining"],
    provider["time"],
    provider["playStandardEvents"]
  )(provider["event"])

  assert result == provider["expectedCanPlayEvent"]

def test_cannotPlayEventIfItFormsAGroupAndThereAreOnlyTwoTributes():
  event = { "formGroup": True }
  tribute = {}
  playersRemaining = { "Player2": {} }
  time = "day"
  playStandardEvents = True

  vars.tributes = [ "Player1", "Player2" ]

  result = canPlayEvent(tribute, playersRemaining, time, playStandardEvents)(event)

  assert result == False

def test_cannotPlayEventIfTheTributeDoesNotHaveTheRequiredPossessions(mocker):
  mocker.patch( "canPlayEvent.checkHasRequiredPossessions", return_value=False )

  result = canPlayEvent({}, {}, "day", True)({})

  assert result == False

def test_cannotPlayEventIfTheTributeDoesNotComplyWithTheRequiredGroupSize(mocker):
  mocker.patch( "canPlayEvent.checkCompliesWithRequiredGroupSize", return_value=False )

  result = canPlayEvent({}, {}, "day", True)({})

  assert result == False

def test_cannotPlayEventIfTheTributeCannotBetrayTeammates(mocker):
  mocker.patch( "canPlayEvent.checkCanBetrayTeammates", return_value=False )

  result = canPlayEvent({}, {}, "day", True)({})

  assert result == False

def test_cannotPlayEventIfTheTributeCannotPlayTimedEvents(mocker):
  mocker.patch( "canPlayEvent.checkCanPlayTimedEvents", return_value=False )

  result = canPlayEvent({}, {}, "day", True)({})

  assert result == False
