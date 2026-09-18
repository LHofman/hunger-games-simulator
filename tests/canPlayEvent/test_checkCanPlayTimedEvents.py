import pytest
from canPlayEvent import checkCanPlayTimedEvents

providers = [
  ({
    "id": "An event can be played if the event time matches the current time",
    "event": { "time": "Day" },
    "time": "Day",
    "playStandardEvents": None,
    "expectedCanPlayTimedEvents": True,
  }),
  ({
    "id": "An event cannot be played if the event time does not match the current time",
    "event": { "time": "Day" },
    "time": "Night",
    "playStandardEvents": None,
    "expectedCanPlayTimedEvents": False,
  }),
  ({
    "id": "An event can be played if the event time is a list and the current time is in that list",
    "event": { "time": ["Day", "Night"] },
    "time": "Night",
    "playStandardEvents": None,
    "expectedCanPlayTimedEvents": True,
  }),
  ({
    "id": "An event cannot be played if the event time is a list and the current time is not in that list",
    "event": { "time": ["Day", "Night"] },
    "time": "Feast",
    "playStandardEvents": None,
    "expectedCanPlayTimedEvents": False,
  }),
  ({
    "id": "An event can be played if the event time is not specified and standard events are allowed",
    "event": {},
    "time": "Day",
    "playStandardEvents": True,
    "expectedCanPlayTimedEvents": True,
  }),
  ({
    "id": "An event cannot be played if the event time is not specified and standard events are not allowed",
    "event": {},
    "time": "Day",
    "playStandardEvents": False,
    "expectedCanPlayTimedEvents": False,
  }),
]

@pytest.mark.parametrize("provider", providers, ids=lambda p: f"{p['id']}")
def test_checkCanPlayTimedEvents(provider):
  result = checkCanPlayTimedEvents(
    provider["time"],
    provider["event"],
    provider["playStandardEvents"]
  )
  assert result == provider["expectedCanPlayTimedEvents"]
