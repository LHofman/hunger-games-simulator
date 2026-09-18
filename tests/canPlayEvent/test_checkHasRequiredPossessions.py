import pytest
from canPlayEvent import checkHasRequiredPossessions

# Mock tribute possessions, alsways has "Test Item 1" and "Test Item 2"
@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch(
    "canPlayEvent.hasPossession",
    side_effect=lambda tribute, type, value: value in ['Test Item 1', 'Test Item 2']
  )

providers = [
  ({
    "id": "an event without required possessions can be played",
    "event": { "name": "Test Event" },
    "expectedHasRequiredPossessions": True,
  }),
  ({
    "id": "an event with a required possession that the tribute has can be played",
    "event": { "name": "Test Event", "requiresPossessions": [{ "type": "item", "value": "Test Item 1" }] },
    "expectedHasRequiredPossessions": True,
  }),
  ({
    "id": "an event with a required possession that the tribute does not have cannot be played",
    "event": { "name": "Test Event", "requiresPossessions": [{ "type": "item", "value": "Test Item 3" }] },
    "expectedHasRequiredPossessions": False,
  }),
  ({
    "id": "an event with a required possession that the tribute does not have but is negated can be played",
    "event": { "name": "Test Event", "requiresPossessions": [{ "type": "item", "value": "Test Item 3", "not": True }] },
    "expectedHasRequiredPossessions": True,
  }),
  ({
    "id": "an event with a required possession that the tribute has but is negated cannot be played",
    "event": { "name": "Test Event", "requiresPossessions": [{ "type": "item", "value": "Test Item 1", "not": True }] },
    "expectedHasRequiredPossessions": False,
  }),
  ({
    "id": "an event with multiple required possessions that the tribute has can be played",
    "event": { "name": "Test Event", "requiresPossessions": [{ "type": "item", "value": "Test Item 1" }, { "type": "item", "value": "Test Item 2" }] },
    "expectedHasRequiredPossessions": True,
  }),
  ({
    "id": "an event with multiple required possessions that the tribute does not have cannot be played",
    "event": { "name": "Test Event", "requiresPossessions": [{ "type": "item", "value": "Test Item 1" }, { "type": "item", "value": "Test Item 3" }] },
    "expectedHasRequiredPossessions": False,
  }),
  ({
    "id": "an event with multiple required possessions that the tribute has and does not have but is negated can be played",
    "event": { "name": "Test Event", "requiresPossessions": [{ "type": "item", "value": "Test Item 1" }, { "type": "item", "value": "Test Item 3", "not": True }] },
    "expectedHasRequiredPossessions": True,
  }),
  ({
    "id": "an event with multiple required possessions that the tribute has and does have but is negated cannot be played",
    "event": { "name": "Test Event", "requiresPossessions": [{ "type": "item", "value": "Test Item 1" }, { "type": "item", "value": "Test Item 2", "not": True }] },
    "expectedHasRequiredPossessions": False,
  }),
  ({
    "id": "an event with multiple required possessions that the tribute does not have and does have but is negated cannot be played",
    "event": { "name": "Test Event", "requiresPossessions": [{ "type": "item", "value": "Test Item 3" }, { "type": "item", "value": "Test Item 4", "not": True }] },
    "expectedHasRequiredPossessions": False,
  })
]

@pytest.mark.parametrize("provider", providers, ids=lambda p: f"{p['id']}")
def test_checkHasRequiredPossessions(provider):
  result = checkHasRequiredPossessions({}, provider["event"])
  assert result == provider["expectedHasRequiredPossessions"]
