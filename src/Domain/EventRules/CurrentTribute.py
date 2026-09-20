"""Event rule that handles effects on the gamestate based on the current tribute."""

from Domain.EventRule import EventRule, TextAndTerms
from Domain.types import GameRoundState


class CurrentTribute(EventRule):
    """Event rule that handles effects on the gamestate based on the current tribute."""

    def replaceTextTerms(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms,
    ) -> TextAndTerms:
        """Replace text and terms in the event based on the current tribute."""
        text = textAndTerms['text'].replace(
            '(Player1)',
            gameState['currentTribute']['name'],
        )

        return {
            **textAndTerms,
            'text': text,
            'players': [gameState['currentTribute']],
        }
