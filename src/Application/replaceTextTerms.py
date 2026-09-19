from Domain.EventRule import TextAndTerms
from Domain.eventRulesList import eventRulesList
from Domain.types import GameRoundState


def replaceTextTerms(gameState: GameRoundState) -> TextAndTerms:
    textAndTerms: TextAndTerms = {
        'text': gameState['event']['text'],
        'players': [],
        'terms': {}
    }

    for eventRule in eventRulesList:
        textAndTerms = eventRule.replaceTextTerms(gameState, textAndTerms)
            
    return textAndTerms
