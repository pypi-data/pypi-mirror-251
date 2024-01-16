from fugo import Meter


def test_parsing():
    expected = {
        '2/2': Meter(2, 2),
        '3/4': Meter(3, 4),
        '7/8': Meter(7, 8),
    }

    for string, meter in expected.items():
        assert Meter.from_string(string) == meter
