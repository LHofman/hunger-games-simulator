from typing import Union
from Domain.EventRule import EventRule, TextAndTerms
from Domain.types import GameRoundState, Tribute

class TributesData(EventRule):
  def handleEventEffects(self, gameState: GameRoundState, textAndTerms: TextAndTerms) -> None:
    event = gameState['event']

    if ('updateTributesData' not in event): return

    for dataToAdd in event['updateTributesData']:
      self.updateTributesData(
        gameState,
        gameState['playersAlive'][textAndTerms.get('players', [])[dataToAdd['player'] - 1]['name']],
        dataToAdd['type'],
        dataToAdd['operation'] if ('operation' in dataToAdd) else '',
        dataToAdd['value']
      )

  @staticmethod
  def updateTributesData(
    gameState: GameRoundState,
    tribute: Tribute,
    type: str,
    operation: str,
    value: Union[int, str]
  ):
    if (tribute['name'] not in gameState['tributesData']):
      gameState['tributesData'][tribute['name']] = {}
    
    if (type not in gameState['tributesData'][tribute['name']]):
      gameState['tributesData'][tribute['name']][type] = value
      return

    if (operation == 'add'):
      gameState['tributesData'][tribute['name']][type] += value # type: ignore
    elif (operation == 'remove'):
      gameState['tributesData'][tribute['name']][type] -= value # type: ignore
    else:
      gameState['tributesData'][tribute['name']][type] = value
      