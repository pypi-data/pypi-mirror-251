from fractions import Fraction

from fugo import Meter, WHOLE, HALF, QUARTER, EIGHTH, SIXTEENTH
from fugo import Clock, Time


def test_clock_tick_4_4():
    clock = Clock(meter=Meter(4, 4))
    assert clock.time == Time(1, 1)

    clock.tick(WHOLE)
    assert clock.time == Time(2, 1)

    clock.tick(HALF)
    assert clock.time == Time(2, 3)

    clock.tick(QUARTER)
    assert clock.time == Time(2, 4)

    clock.tick(EIGHTH)
    assert clock.time == Time(2, 4, Fraction(1, 2))

    clock.tick(SIXTEENTH)
    assert clock.time == Time(2, 4, Fraction(3, 4))

    clock.tick(EIGHTH)
    assert clock.time == Time(3, 1, Fraction(1, 4))


def test_clock_tick_6_8():
    clock = Clock(meter=Meter(6, 8))
    assert clock.time == Time(1, 1)

    clock.tick(WHOLE + HALF)
    assert clock.time == Time(3, 1)

    clock.tick(WHOLE)
    assert clock.time == Time(4, 3)

    clock.tick(HALF)
    assert clock.time == Time(5, 1)

    clock.tick(QUARTER)
    assert clock.time == Time(5, 3)

    clock.tick(EIGHTH)
    assert clock.time == Time(5, 4)

    clock.tick(SIXTEENTH)
    assert clock.time == Time(5, 4, Fraction(1, 2))

    clock.tick(EIGHTH)
    assert clock.time == Time(5, 5, Fraction(1, 2))
