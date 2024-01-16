__all__ = ['Time', 'Clock']

from fractions import Fraction
from typing import NamedTuple

from fugo import Duration, Meter


class Time(NamedTuple):
    """Represent score position."""

    measure: int
    beat: int
    pulse: Fraction | int = 0


class Clock:
    """Provide context for `Time` objects."""

    def __init__(self, meter: Meter = Meter(4, 4)):
        self.meter = meter
        self._time = 0

    def tick(self, duration: Duration) -> Time:
        self._time += duration
        return self.time

    @property
    def time(self) -> Time:
        METER = Fraction(self.meter.beats, self.meter.division)

        measure, _beat = divmod(self._time, METER)
        beat, pulse = divmod(_beat * self.meter.division, 1)

        return Time(measure + 1, beat + 1, pulse)
