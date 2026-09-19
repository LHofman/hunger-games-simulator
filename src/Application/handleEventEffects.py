from Domain.EventRule import TextAndTerms
from Domain.eventRulesList import eventRulesList
from Domain.types import GameRoundState


def handleEventEffects(
    gameState: GameRoundState,
    textAndTerms: TextAndTerms
) -> None:
    for eventRule in eventRulesList:
        eventRule.handleEventEffects(gameState, textAndTerms)
