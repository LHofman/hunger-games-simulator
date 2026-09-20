"""Represent a tribute in the Hunger Games."""

from __future__ import annotations

from dataclasses import dataclass, field

from domain.types import GameOptions


@dataclass
class Tribute:
    """Represent a tribute in the Hunger Games."""

    index: int
    name: str
    district: int
    grouped_with: list[str] = field(default_factory=list[str])
    possessions: dict[str, list[str]] = field(
        default_factory=dict[str, list[str]]
    )
    kills: int = 0
    time_of_death: str | None = None

    def add_possession(
        self,
        gameOptions: GameOptions,
        possession_type: str,
        value: str,
    ):
        if possession_type not in self.possessions:
            self.possessions[possession_type] = [value]
            return

        if (
            possession_type
            not in (gameOptions['possessions_without_duplicates'])
        ):
            self.possessions[possession_type].append(value)

    def remove_possession(
        self,
        possession_type: str,
        value: str,
    ):
        if self.has_possession(possession_type, value):
            self.possessions[possession_type].remove(value)

    def has_possession(self, type: str, value: str) -> bool:
        """Check if the tribute has the specified possession."""
        if value == 'any':
            return type in self.possessions and len(self.possessions[type]) > 0

        return type in self.possessions and value in self.possessions[type]

    def group_with(self, other_tribute_name: str):
        """Group this tribute with another tribute."""
        if other_tribute_name not in self.grouped_with:
            self.grouped_with.append(other_tribute_name)

    def ungroup_with(self, other_tribute_name: str):
        """Ungroup this tribute from another tribute."""
        if other_tribute_name in self.grouped_with:
            self.grouped_with.remove(other_tribute_name)

    def is_grouped_with(self, other_tribute_name: str) -> bool:
        """Check if this tribute is grouped with another tribute."""
        return other_tribute_name in self.grouped_with

    def ungroup_all(self):
        """Ungroup this tribute from all other tributes."""
        self.grouped_with.clear()

    def mark_dead(self, time_of_death: str):
        """Mark this tribute as dead and record the time of death."""
        self.time_of_death = time_of_death

    def add_kills(self, number_of_kills: int = 1):
        """Add kills to this tribute's kill count."""
        self.kills += number_of_kills
