from fugo import NoteName
from fugo import Degree, Mode, Key


def test_parsing():
    expected = {
        'C': Key.from_attrs(NoteName('C'), Mode.MAJOR),
        'd#': Key.from_attrs(NoteName('D#'), Mode.MINOR),
        'ebbM': Key.from_attrs(NoteName('Ebb'), Mode.MAJOR),
        'FM': Key.from_attrs(NoteName('F'), Mode.MAJOR),
        'gm': Key.from_attrs(NoteName('G'), Mode.MINOR),
        'Ab dorian': Key.from_attrs(NoteName('Ab'), Mode.DORIAN),
        'B-major': Key.from_attrs(NoteName('B'), Mode.MAJOR),
        'C#-minor': Key.from_attrs(NoteName('C#'), Mode.MINOR),
    }

    for string, note in expected.items():
        assert Key.from_string(string) == note


def test_contains():
    assert NoteName('C') in Key('Cm')
    assert NoteName('C#') in Key('D')
    assert NoteName('Bb') not in Key('D dorian')
    assert NoteName('B') in Key('D dorian')


def test_get_degree():
    assert Key('Fm')[Degree(1)] == NoteName('F')
    assert Key('Eb')[Degree(2)] == NoteName('F')
    assert Key('A')[Degree(3)] == NoteName('C#')
    assert Key('C lydian')[Degree(4)] == NoteName('F#')
    assert Key('D')[Degree(5)] == NoteName('A')
    assert Key('G#m')[Degree(6)] == NoteName('E')
    assert Key('B')[Degree.LEADING_TONE] == NoteName('A#')
    assert Key('B')[Degree.SUBTONIC] == NoteName('A')
    assert Key('B')[Degree(7)] == NoteName('A#')
