from Domain.types import GameRoundState
from Domain.EventRule import TextAndTerms
from Domain.eventRulesList import eventRulesList


def replaceTextTerms(gameState: GameRoundState) -> TextAndTerms:
    textAndTerms: TextAndTerms = {
        'text': gameState['event']['text'],
        'players': [],
        'terms': {}
    }

    for eventRule in eventRulesList:
        textAndTerms = eventRule.replaceTextTerms(gameState, textAndTerms)
            
    return textAndTerms
