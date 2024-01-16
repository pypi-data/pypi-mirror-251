from fugo import Accidental, LetterName
from fugo import Interval, Note


def test_parsing():
    expected = {
        'C4': Note.from_attrs(LetterName.C, Accidental.NATURAL, 4),
        'd#4': Note.from_attrs(LetterName.D, Accidental.SHARP, 4),
        'ebb-20': Note.from_attrs(LetterName.E, Accidental.DOUBLE_FLAT, -20),
        'bb-20': Note.from_attrs(LetterName.B, Accidental.FLAT, -20),
    }

    for string, note in expected.items():
        assert Note.from_string(string) == note


def test_pitch():
    """Test the `Note.pitch` property."""
    expected = {
        Note('C4'): 60,
        Note('Dbb4'): 60,
        Note('B#3'): 60,
        Note('C-1'): 0,
    }

    for note, number in expected.items():
        assert note.pitch == number


def test_comparisons():
    """Test the `Note` rich comparison methods."""
    assert Note('A4') < Note('B4')
    assert Note('C#4') < Note('Dbb4')
    assert Note('C3') <= Note('C4')
    assert Note('E2') == Note('E2')
    assert Note('E2') != Note('Fb2')
    assert Note('C8') > Note('D7')
    assert Note('Cb4') >= Note('B3')


def test_addition():
    """Test `Note` + `Interval` addition."""
    cases = [
        ('Cb5', 'd1', 'Cbb5'),
        ('Cb5', 'P5', 'Gb5'),
        ('C#2', 'd8', 'C3'),
        ('C-1', 'P8', 'C0'),
        ('Cb3', 'A8', 'C4'),
        ('Cb5', 'A8', 'C6'),
        ('D8', 'P1', 'D8'),
        ('D#2', 'm6', 'B2'),
        ('Eb3', 'm6', 'Cb4'),
        ('E6', 'm6', 'C7'),
        ('F2', 'M3', 'A2'),
        ('G8', 'd2', 'Abb8'),
        ('G#3', 'P4', 'C#4'),
        ('G#9', 'M2', 'A#9'),
        ('A4', 'P5', 'E5'),
        ('A#7', 'm2', 'B7'),
        ('B#4', 'd1', 'B4'),
        ('B#6', 'P1', 'B#6'),
        ('B#4', 'P5', 'Fx5'),
    ]

    for a, b, c in cases:
        assert Note(a) + Interval(b) == Note(c), Note(a) + Interval(b)


def test_subtraction():
    """Test `Note` - `Interval` subtraction."""
    cases = [
        ('C5', 'P5', 'F4'),
        ('C#2', 'M3', 'A1'),
        ('D8', 'P8', 'D7'),
        ('Eb4', 'm2', 'D4'),
        ('E-1', 'M3', 'C-1'),
        ('F6', 'P1', 'F6'),
        ('G2', 'm6', 'B1'),
        ('Ab3', 'P4', 'Eb3'),
        ('Bb9', 'M7', 'Cb9'),
    ]

    for a, b, c in cases:
        assert Note(a) - Interval(b) == Note(c), Note(a) - Interval(b)
