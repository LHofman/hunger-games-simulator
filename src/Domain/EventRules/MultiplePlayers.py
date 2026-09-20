"""Event rule that handles effects on the gamestate based on multiple players involved in an event."""

import random

from Domain.EventRule import EventRule, TextAndTerms
from Domain.types import Event, GameRoundState, GameRoundStateWithoutEvent


class MultiplePlayers(EventRule):
    """Event rule that handles effects on the gamestate based on multiple players involved in an event."""

    def canPlayEvent(
        self,
        event: Event,
        gameState: GameRoundStateWithoutEvent,
    ) -> bool:
        """Check if the event can be played based on the number of players involved in the event."""
        if 'players' not in event: return True

        return (
            len(gameState['playersRemainingThisRound']) + 1
            >= event['players']
        )

    def replaceTextTerms(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms,
    ) -> TextAndTerms:
        """Replace text and terms in the event based on the number of players involved in the event."""
        text = textAndTerms['text']
        players = textAndTerms.get('players', [])

        while (text.find('(Player') > -1):
            player = random.choice(
                list(gameState['playersRemainingThisRound'].values()),
            )
            del gameState['playersRemainingThisRound'][player['name']]

            players.append(player)
            text = text.replace(f'(Player{len(players)})', player['name'])

        return { **textAndTerms, 'text': text, 'players': players }
