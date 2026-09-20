"""Event rule that handles effects on the gamestate based on group dynamics."""

import random
import re

from domain.event_rule import EventRule, TextAndTerms
from domain.types import (
    Event,
    GameRoundState,
    GameRoundStateWithoutEvent,
    GroupSizeType,
    Tribute,
)


class Groups(EventRule):
    """Event rule that handles effects on the gamestate based on group dynamics."""

    def can_play_event(
        self,
        event: Event,
        game_state: GameRoundStateWithoutEvent,
    ) -> bool:
        """Check if the event can be played based on group dynamics and game state."""
        if not self._satisfies_group_size(event, game_state): return False
        if not self._satisfies_can_form_group(event, game_state): return False
        if not self._satisfies_can_betray_teammates(event, game_state):
            return False

        return True

    def _satisfies_group_size(
        self,
        event: Event,
        game_state: GameRoundStateWithoutEvent,
    ) -> bool:
        if 'require_group_size' not in event: return True

        size_type = event['require_group_size']['type']
        size = event['require_group_size']['amount']

        available_group_tributes = 1  # Tribute themself.
        for (name) in game_state['players_remaining_this_round'].keys():
            if name in game_state['current_tribute']['grouped_with']:
                available_group_tributes += 1

        if (
            size_type == GroupSizeType.EXACT
            and size != len(game_state['current_tribute']['grouped_with']) + 1
        ): return False

        if (
            size_type == GroupSizeType.MIN
            and size > available_group_tributes
        ): return False

        if (
            size_type == GroupSizeType.MAX
            and size < len(game_state['current_tribute']['grouped_with']) + 1
        ): return False

        return True

    def _satisfies_can_form_group(
        self,
        event: Event,
        game_state: GameRoundStateWithoutEvent,
    ) -> bool:
        if 'form_group' not in event: return True

        return len(game_state['players_alive']) > 2
    
    def _satisfies_can_betray_teammates(
        self,
        event: Event,
        game_state: GameRoundStateWithoutEvent,
    ) -> bool:
        if game_state['options']['betray_teammates']: return True
        if 'deaths' not in event: return True
        if 'kill_teammates' not in event or not event['kill_teammates']:
            return True

        for death in event['deaths']:
            if death in game_state['current_tribute']['grouped_with']:
                return False

        return True

    def replace_text_terms(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> TextAndTerms:
        """Replace text and terms in the event based on group dynamics and the current game state."""
        event = game_state['event']

        if 'require_group_size' not in event: return text_and_terms

        ao_group_players_required = event['require_group_size']['amount']
        
        players_remaining = game_state.get('players_remaining_this_round').items()
        grouped_with_players: dict[str, Tribute] = {}
        for (name, player) in players_remaining:
            if name in game_state.get('current_tribute')['grouped_with']:
                grouped_with_players[name] = player

        text = text_and_terms['text']
        players: list[Tribute] = text_and_terms.get('players', [])
        while (
            text.find('(Player') > -1
            and len(players) < ao_group_players_required
        ):
            player = random.choice(list(grouped_with_players.values()))
            del grouped_with_players[player['name']]
            del game_state['players_remaining_this_round'][player['name']]

            players.append(player)
            text = text.replace(f'(Player{len(players)})', player['name'])

        return { **text_and_terms, 'text': text, 'players': players }

    def handle_event_effects(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> None:
        """Handle the effects of group dynamics in the event on the game state."""
        self._handle_form_group(game_state, text_and_terms.get('players', []))
        self._handle_split_group(game_state, text_and_terms.get('players', []))

    def _handle_form_group(
        self,
        game_state: GameRoundState,
        players: list[Tribute],
    ) -> None:
        event = game_state['event']

        if 'form_group' not in event: return

        for player in players:
            for other_player in players:
                if player['name'] == other_player['name']: continue

                grouped_with = (
                    game_state['players_alive'][player['name']]['grouped_with']
                )
                if other_player['name'] in grouped_with: continue
                grouped_with.append(other_player['name'])

    def _handle_split_group(
        self,
        game_state: GameRoundState,
        players: list[Tribute],
    ) -> None:
        event = game_state['event']

        if 'split_group' not in event: return

        players_to_split: list[str] = []
        for player_to_split in event['split_group']:
            match = re.search(r'\d+', player_to_split)
            if not match: raise ValueError(
                f'No number found in split group term: {player_to_split}',
            )

            index = int(match.group()) - 1
            players_to_split.append(players[index]['name'])
            
        for player in players:
            if player['name'] not in players_to_split: continue
            for player_to_split in players_to_split:
                if player_to_split != player['name']:
                    grouped_tribute = (
                        game_state['players_alive'][player['name']]
                    )
                    grouped_tribute['grouped_with'].remove(player_to_split)
