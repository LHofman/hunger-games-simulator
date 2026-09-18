import pytest
import random
import vars
from getEventTextPlayersAndTerms import setSponsorsNames

@pytest.fixture(autouse=True)
def test_mock(mocker):
  mocker.patch.object( vars, "totalTributes", 2 )

  mocker.patch(
    "random.choice",
    side_effect=lambda list: list[0]
  )

providers = [
  ({
    "id": "Text without (Sponsor) placeholder doesn't change.",
    "text": "Tribute explores the arena.",
    "1SponsorPerTribute": True,
    "tribute": {"index": 2},
    "sponsors": ["Sponsor1", "Sponsor2"],
    "expectedText": "Tribute explores the arena.",
  }),
  ({
    "id": "If the option 1SponsorPerTribute is disabled, a random sponsor is chosen",
    "text": "Tribute receives a bow, some arrows, and a quiver from (Sponsor).",
    "1SponsorPerTribute": False,
    "tribute": {"index": 2},
    "sponsors": ["Sponsor1", "Sponsor2"],
    "expectedText": "Tribute receives a bow, some arrows, and a quiver from Sponsor1.",
  }),
  ({
    "id": "If there are more sponsors than tributes, a random sponsor is chosen",
    "text": "Tribute receives a bow, some arrows, and a quiver from (Sponsor).",
    "1SponsorPerTribute": True,
    "tribute": {"index": 2},
    "sponsors": ["Sponsor1", "Sponsor2", "Sponsor3"],
    "expectedText": "Tribute receives a bow, some arrows, and a quiver from Sponsor1.",
  }),
  ({
    "id": "If there are less sponsors than tributes, a random sponsor is chosen",
    "text": "Tribute receives a bow, some arrows, and a quiver from (Sponsor).",
    "1SponsorPerTribute": True,
    "tribute": {"index": 2},
    "sponsors": ["Sponsor3"],
    "expectedText": "Tribute receives a bow, some arrows, and a quiver from Sponsor3.",
  }),
  ({
    "id": "A tribute receives an item from their respective sponsor",
    "text": "Tribute receives a bow, some arrows, and a quiver from (Sponsor).",
    "1SponsorPerTribute": True,
    "tribute": {"index": 2},
    "sponsors": ["Sponsor1", "Sponsor2"],
    "expectedText": "Tribute receives a bow, some arrows, and a quiver from Sponsor2.",
  }),
  ({
    "id": "A tribute receives an item from an opposing sponsor",
    "text": "Tribute receives a bow, some arrows, and a quiver from (Sponsor::opposing).",
    "1SponsorPerTribute": True,
    "tribute": {"index": 2},
    "sponsors": ["Sponsor1", "Sponsor2"],
    "expectedText": "Tribute receives a bow, some arrows, and a quiver from Sponsor1.",
  }),
]

@pytest.mark.parametrize("provider", providers, ids=lambda p: f"{p['id']}")
def test_setSponsorsNames(provider, mocker):
  vars.gameData["options"] = { "1SponsorPerTribute": provider["1SponsorPerTribute"] }
  vars.sponsors = provider["sponsors"]

  result = setSponsorsNames(
    provider["tribute"],
    provider["text"],
  )

  assert result == provider["expectedText"]
