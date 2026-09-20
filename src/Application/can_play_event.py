"""Check if an event can be played in the given game state."""

from domain.event_rules_list import event_rules_list
from domain.types import Event, GameRoundStateWithoutEvent


def can_play_event(game_state: GameRoundStateWithoutEvent):
    """Return a function that checks if an event can be played in the given game state."""

    def can_play_event_inner(event: Event) -> bool:
        for event_rule in event_rules_list:
            if not event_rule.can_play_event(event, game_state):
                return False
            
        return True

    return can_play_event_inner
