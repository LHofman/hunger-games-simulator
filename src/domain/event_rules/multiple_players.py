"""Event rule that handles effects on the gamestate based on multiple players involved in an event."""

import random

from domain.event_rule import EventRule, TextAndTerms
from domain.types import Event, GameRoundState, GameRoundStateWithoutEvent


class MultiplePlayers(EventRule):
    """Event rule that handles effects on the gamestate based on multiple players involved in an event."""

    def can_play_event(
        self,
        event: Event,
        game_state: GameRoundStateWithoutEvent,
    ) -> bool:
        """Check if the event can be played based on the number of players involved in the event."""
        if 'players' not in event: return True

        return (
            len(game_state['players_remaining_this_round']) + 1
            >= event['players']
        )

    def replace_text_terms(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> TextAndTerms:
        """Replace text and terms in the event based on the number of players involved in the event."""
        text = text_and_terms['text']
        players = text_and_terms.get('players', [])

        while (text.find('(Player') > -1):
            player = random.choice(
                list(game_state['players_remaining_this_round'].values()),
            )
            del game_state['players_remaining_this_round'][player['name']]

            players.append(player)
            text = text.replace(f'(Player{len(players)})', player['name'])

        return { **text_and_terms, 'text': text, 'players': players }
