__all__ = [
    'Duration',
    'WHOLE',
    'HALF',
    'QUARTER',
    'EIGHTH',
    'SIXTEENTH',
]

from fractions import Fraction


class Duration(Fraction):
    """Represent the length of a note, rest, or other event.

    notes:
        - `Duration`s are relative to the length of a whole note (1)
            - quarter: 1/4
            - dotted quarter: 1/4 + 1/8 == 3/8
            - eighth triplet: 1/4 / 3 == 1/12
        - `Duration`s are independent of meter
            - the length of an eight note is 1/8 in 2/2, 3/4, and 7/8
    """

    def __add__(self, other) -> 'Duration':
        return Duration(super().__add__(other))

    def __radd__(self, other) -> 'Duration':
        return Duration(super().__radd__(other))

    def __sub__(self, other) -> 'Duration':
        return Duration(super().__sub__(other))

    def __rsub__(self, other) -> 'Duration':
        return Duration(super().__rsub__(other))

    def __mul__(self, other) -> 'Duration':
        return Duration(super().__mul__(other))

    def __rmul__(self, other) -> 'Duration':
        return Duration(super().__rmul__(other))

    def __truediv__(self, other) -> 'Duration':
        return Duration(super().__truediv__(other))

    def __rtruediv__(self, other) -> 'Duration':
        return Duration(super().__rtruediv__(other))

    def __floordiv__(self, other) -> 'Duration':
        return Duration(super().__floordiv__(other))

    def __rfloordiv__(self, other) -> 'Duration':
        return Duration(super().__rfloordiv__(other))

    def __mod__(self, other) -> 'Duration':
        return Duration(super().__mod__(other))

    def __rmod__(self, other) -> 'Duration':
        return Duration(super().__rmod__(other))

    def __divmod__(self, other) -> tuple[int | float, 'Duration']:
        quotient, remainder = super().__divmod__(other)
        return quotient, Duration(remainder)

    def __rdivmod__(self, other: float) -> tuple[int | float, 'Duration']:
        quotient, remainder = super().__rdivmod__(other)
        return quotient, Duration(remainder)


WHOLE = Duration(1)
HALF = Duration(1, 2)
QUARTER = Duration(1, 4)
EIGHTH = Duration(1, 8)
SIXTEENTH = Duration(1, 16)
