__all__ = ['Meter']

from dataclasses import dataclass


@dataclass
class Meter:
    """Represent a meter (time signature)."""

    beats: int
    division: int

    @classmethod
    def from_string(cls, s: str, /) -> 'Meter':
        top, bottom = map(int, s.split('/'))
        return cls(top, bottom)
