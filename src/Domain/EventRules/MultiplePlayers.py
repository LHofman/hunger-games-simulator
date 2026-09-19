import random
from Domain.EventRule import EventRule, TextAndTerms
from Domain.types import Event, GameRoundState, GameRoundStateWithoutEvent

class MultiplePlayers(EventRule):
  def canPlayEvent(
    self,
    event: Event,
    gameState: GameRoundStateWithoutEvent
  ) -> bool:
    if 'players' not in event: return True

    return len(gameState['playersRemainingThisRound']) + 1 >= event['players']

  def replaceTextTerms(self, gameState: GameRoundState, textAndTerms: TextAndTerms) -> TextAndTerms:
    text = textAndTerms['text']
    players = textAndTerms.get('players', [])

    while (text.find('(Player') > -1):
      player = random.choice(list(gameState['playersRemainingThisRound'].values()))
      del gameState['playersRemainingThisRound'][player['name']]

      players.append(player)
      text = text.replace('(Player%d)' % len(players), player['name'])

    return { **textAndTerms, 'text': text, 'players': players }
