from fugo import WHOLE, HALF, QUARTER, EIGHTH, SIXTEENTH


def test_operators():
    assert QUARTER + QUARTER == HALF
    assert WHOLE - QUARTER - QUARTER == HALF
    assert 4 * SIXTEENTH == QUARTER
    assert EIGHTH / 2 == SIXTEENTH
    assert (HALF + EIGHTH) % HALF == EIGHTH
