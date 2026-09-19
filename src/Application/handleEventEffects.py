from Domain.types import GameRoundState
from Domain.EventRule import TextAndTerms
from Domain.eventRulesList import eventRulesList


def handleEventEffects(
    gameState: GameRoundState,
    textAndTerms: TextAndTerms
) -> None:
    for eventRule in eventRulesList:
        eventRule.handleEventEffects(gameState, textAndTerms)
