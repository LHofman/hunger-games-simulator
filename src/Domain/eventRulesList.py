from Domain.EventRule import EventRule
from Domain.EventRules.CurrentTribute import CurrentTribute
from Domain.EventRules.Deaths import Deaths
from Domain.EventRules.Groups import Groups
from Domain.EventRules.IgnoreComments import IgnoreComments
from Domain.EventRules.MultiplePlayers import MultiplePlayers
from Domain.EventRules.OtherTerms import OtherTerms
from Domain.EventRules.Possessions import Possessions
from Domain.EventRules.Sponsors import Sponsors
from Domain.EventRules.TimedEvents import TimedEvents
from Domain.EventRules.TributesData import TributesData

# The order is important
eventRulesList: list[EventRule] = [
    IgnoreComments(),
    TimedEvents(),

    # Needs to be before Groups and MultiplePlayers
    CurrentTribute(),
    # Needs to be after CurrentTribute and before MultiplePlayers
    Groups(),
    # Needs to be after CurrentTribute and Groups
    MultiplePlayers(),

    Possessions(),
    OtherTerms(),
    Sponsors(),
    TributesData(),
    Deaths(),
]