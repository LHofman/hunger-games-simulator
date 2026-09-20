"""Event rules list for the hunger games simulator."""

from domain.event_rule import EventRule
from domain.event_rules.current_tribute import CurrentTribute
from domain.event_rules.deaths import Deaths
from domain.event_rules.groups import Groups
from domain.event_rules.ignore_comments import IgnoreComments
from domain.event_rules.multiple_tributes import MultipleTributes
from domain.event_rules.other_terms import OtherTerms
from domain.event_rules.possessions import Possessions
from domain.event_rules.sponsors import Sponsors
from domain.event_rules.timed_events import TimedEvents
from domain.event_rules.tributes_data import TributesData

# The order is important.
event_rules_list: list[EventRule] = [
    IgnoreComments(),
    TimedEvents(),
    # Needs to be before Groups and MultipleTributes.
    CurrentTribute(),
    # Needs to be after current_tribute and before MultipleTributes.
    Groups(),
    # Needs to be after current_tribute and Groups.
    MultipleTributes(),
    Possessions(),
    OtherTerms(),
    Sponsors(),
    TributesData(),
    Deaths(),
]
