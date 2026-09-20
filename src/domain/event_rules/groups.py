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
        if not self._satisfies_group_size(event, game_state):
            return False

        if not self._satisfies_can_form_group(event, game_state):
            return False

        return self._satisfies_can_betray_teammates(event, game_state)

    def _satisfies_group_size(
        self,
        event: Event,
        game_state: GameRoundStateWithoutEvent,
    ) -> bool:
        if 'require_group_size' not in event:
            return True

        size_type = event['require_group_size']['type']
        size = event['require_group_size']['amount']

        available_group_tributes = 1  # Tribute themself.
        for name in game_state['tributes_remaining_this_round']:
            if name in game_state['current_tribute']['grouped_with']:
                available_group_tributes += 1

        if (
            size_type == GroupSizeType.EXACT
            and size != len(game_state['current_tribute']['grouped_with']) + 1
        ):
            return False

        if size_type == GroupSizeType.MIN and size > available_group_tributes:
            return False

        if (
            size_type == GroupSizeType.MAX
            and size < len(game_state['current_tribute']['grouped_with']) + 1
        ):
            return False

        return True

    def _satisfies_can_form_group(
        self,
        event: Event,
        game_state: GameRoundStateWithoutEvent,
    ) -> bool:
        if 'form_group' not in event:
            return True

        return len(game_state['tributes_alive']) > 2

    def _satisfies_can_betray_teammates(
        self,
        event: Event,
        game_state: GameRoundStateWithoutEvent,
    ) -> bool:
        if game_state['options']['betray_teammates']:
            return True
        if 'deaths' not in event:
            return True
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

        if 'require_group_size' not in event:
            return text_and_terms

        ao_group_tributes_required = event['require_group_size']['amount']

        tributes_remaining = game_state.get(
            'tributes_remaining_this_round'
        ).items()
        grouped_with_tributes: dict[str, Tribute] = {}
        for name, tribute in tributes_remaining:
            if name in game_state.get('current_tribute')['grouped_with']:
                grouped_with_tributes[name] = tribute

        text = text_and_terms['text']
        tributes: list[Tribute] = text_and_terms.get('tributes', [])
        while (
            text.find('(Tribute') > -1
            and len(tributes) < ao_group_tributes_required
        ):
            tribute = random.choice(list(grouped_with_tributes.values()))
            del grouped_with_tributes[tribute['name']]
            del game_state['tributes_remaining_this_round'][tribute['name']]

            tributes.append(tribute)
            text = text.replace(f'(Tribute{len(tributes)})', tribute['name'])

        return {**text_and_terms, 'text': text, 'tributes': tributes}

    def handle_event_effects(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> None:
        """Handle the effects of group dynamics in the event on the game state."""
        self._handle_form_group(game_state, text_and_terms.get('tributes', []))
        self._handle_split_group(game_state, text_and_terms.get('tributes', []))

    def _handle_form_group(
        self,
        game_state: GameRoundState,
        tributes: list[Tribute],
    ) -> None:
        event = game_state['event']

        if 'form_group' not in event:
            return

        for tribute in tributes:
            for other_tribute in tributes:
                if tribute['name'] == other_tribute['name']:
                    continue

                grouped_with = game_state['tributes_alive'][tribute['name']][
                    'grouped_with'
                ]
                if other_tribute['name'] in grouped_with:
                    continue
                grouped_with.append(other_tribute['name'])

    def _handle_split_group(
        self,
        game_state: GameRoundState,
        tributes: list[Tribute],
    ) -> None:
        event = game_state['event']

        if 'split_group' not in event:
            return

        tributes_to_split: list[str] = []
        for tribute_to_split in event['split_group']:
            match = re.search(r'\d+', tribute_to_split)
            if not match:
                raise ValueError(
                    f'No number found in split group term: {tribute_to_split}',
                )

            index = int(match.group()) - 1
            tributes_to_split.append(tributes[index]['name'])

        for tribute in tributes:
            if tribute['name'] not in tributes_to_split:
                continue
            for tribute_to_split in tributes_to_split:
                if tribute_to_split != tribute['name']:
                    grouped_tribute = game_state['tributes_alive'][
                        tribute['name']
                    ]
                    grouped_tribute['grouped_with'].remove(tribute_to_split)
