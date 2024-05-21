from typing import Set, Union

from utils.Coverage import Location


class Seed:
    """Represent an input with additional attributes"""

    def __init__(self, data: str, _coverage: Set[Location]) -> None:
        """Initialize from seed data"""
        self.data = data

        # These will be needed for advanced power schedules
        self.coverage: Set[Location] = _coverage
        self.energy = 0.0

    def __str__(self) -> str:
        """Returns data as string representation of the seed"""
        return self.data

    __repr__ = __str__
