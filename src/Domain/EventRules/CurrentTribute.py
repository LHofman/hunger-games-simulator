from Domain.EventRule import EventRule, TextAndTerms
from Domain.types import GameRoundState

class CurrentTribute(EventRule):
    def replaceTextTerms(self, gameState: GameRoundState, textAndTerms: TextAndTerms) -> TextAndTerms:
        text = textAndTerms['text'].replace('(Player1)', gameState['currentTribute']['name'])
        return { **textAndTerms, 'text': text, 'players': [gameState['currentTribute']] }
