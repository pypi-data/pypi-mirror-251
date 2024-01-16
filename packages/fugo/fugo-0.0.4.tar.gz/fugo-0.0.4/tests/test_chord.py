from fugo import Accidental, Interval, Key, NoteName
from fugo import Chord, Quality


def test_parsing():
    expected = {
        Chord('BM'): Chord.from_attrs(NoteName('B'), Quality.MAJOR),
        Chord('Cmaj/E'): Chord.from_attrs(NoteName('C'), Quality.MAJOR, 1),
        Chord('D'): Chord.from_attrs(NoteName('D'), Quality.MAJOR),
        Chord('C#m'): Chord.from_attrs(NoteName('C#'), Quality.MINOR),
        Chord('Emin'): Chord.from_attrs(NoteName('E'), Quality.MINOR),
        Chord('e#'): Chord.from_attrs(NoteName('E#'), Quality.MINOR),
        Chord('F-'): Chord.from_attrs(NoteName('F'), Quality.MINOR),
        Chord('F♯dim'): Chord.from_attrs(NoteName('F#'), Quality.DIMINISHED),
        Chord('G♭º'): Chord.from_attrs(NoteName('Gb'), Quality.DIMINISHED),
        Chord('Go/Db'): Chord.from_attrs(NoteName('G'), Quality.DIMINISHED, 2),
        Chord('G#aug'): Chord.from_attrs(NoteName('G#'), Quality.AUGMENTED),
        Chord('Abb+'): Chord.from_attrs(NoteName('Abb'), Quality.AUGMENTED),
        Chord('a7'): Chord.from_attrs(NoteName('A'), Quality.MAJ_MIN_7),
        Chord('A#Mm7/G#'): Chord.from_attrs(NoteName('A#'), Quality.MAJ_MIN_7, 3),
        Chord('dmaj7'): Chord.from_attrs(NoteName('D'), Quality.MAJ_7),
        Chord('FbM7'): Chord.from_attrs(NoteName('Fb'), Quality.MAJ_7),
        Chord('FΔ'): Chord.from_attrs(NoteName('F'), Quality.MAJ_7),
        Chord('GΔ7/D'): Chord.from_attrs(NoteName('G'), Quality.MAJ_7, 2),
        Chord('Gmin7'): Chord.from_attrs(NoteName('G'), Quality.MIN_7),
        Chord('Em7'): Chord.from_attrs(NoteName('E'), Quality.MIN_7),
        Chord('Bb-7'): Chord.from_attrs(NoteName('Bb'), Quality.MIN_7),
        Chord('CmM7/Eb'): Chord.from_attrs(NoteName('C'), Quality.MIN_MAJ_7, 1),
        Chord('C#-M7'): Chord.from_attrs(NoteName('C#'), Quality.MIN_MAJ_7),
        Chord('F-Δ7/E♮'): Chord.from_attrs(NoteName('F'), Quality.MIN_MAJ_7, 3),
        Chord('bbminmaj7'): Chord.from_attrs(NoteName('Bb'), Quality.MIN_MAJ_7),
        Chord('Ebo7'): Chord.from_attrs(NoteName('Eb'), Quality.DIM_7),
        Chord('Aº7'): Chord.from_attrs(NoteName('A'), Quality.DIM_7),
        Chord('Ddim7/Ab'): Chord.from_attrs(NoteName('D'), Quality.DIM_7, 2),
        Chord('Gø'): Chord.from_attrs(NoteName('G'), Quality.HALF_DIM_7),
        Chord('eø7'): Chord.from_attrs(NoteName('E'), Quality.HALF_DIM_7),
        Chord('Cm7b5'): Chord.from_attrs(NoteName('C'), Quality.HALF_DIM_7),
        Chord('Am7♭5'): Chord.from_attrs(NoteName('A'), Quality.HALF_DIM_7),
        Chord('Fmin7b5/Cb'): Chord.from_attrs(NoteName('F'), Quality.HALF_DIM_7, 2),
        Chord('dbmin7♭5'): Chord.from_attrs(NoteName('Db'), Quality.HALF_DIM_7),
    }

    for parsed, correct in expected.items():
        assert parsed == correct


def test_members():
    def note_names(s: str):
        return [NoteName(n) for n in s.split()]

    expected = {
        Chord('A'): note_names('A C# E'),
        Chord('C#m/E'): note_names('E G# C#'),
        Chord('Gdim/Db'): note_names('Db G Bb'),
        Chord('Cb+'): note_names('Cb Eb G'),
        Chord('C7/Bb'): note_names('Bb C E G'),
        Chord('EM7'): note_names('E G# B D#'),
        Chord('Ebm7'): note_names('Eb Gb Bb Db'),
        Chord('DmM7'): note_names('D F A C#'),
        Chord('Fo7'): note_names('F Ab Cb Ebb'),
        Chord('Bø'): note_names('B D F A'),
    }

    for chord, names in expected.items():
        assert chord.note_names == names


def test_bass():
    cases = {
        'C': 'C',
        'D7': 'D',
        'Em/B': 'B',
        'F#m7': 'F#',
        'G/D': 'D',
    }

    for chord, bass in cases.items():
        assert Chord(chord).bass == NoteName(bass)


def test_intervals():
    def parse(s: str) -> list[Interval]:
        return [Interval(x) for x in s.split()]

    cases = {
        'Cm': 'm3 P5',
        'D': 'M3 P5',
        'Edim': 'm3 d5',
        'F7/C': 'm3 P4 M6',
        'Gm7/Bb': 'M3 P5 M6',
        'A/E': 'P4 M6',
    }

    for chord, intervals in cases.items():
        assert Chord(chord).intervals == parse(intervals)


def test_figures():
    FLAT = Accidental.FLAT
    NATURAL = Accidental.NATURAL
    SHARP = Accidental.SHARP

    chords = {
        'D': {
            'C': [(None, 5), (SHARP, 3)],
            'D': [],
        },
        'Fm': {
            'C': [(None, 5), (FLAT, 3)],
            'c': [],
        },
        'Gdim/Bb': {
            'Ab': [(None, 6)],
            'Bb': [(None, 6), (FLAT, 3)],
            'bb': [(NATURAL, 6)],
        },
        'F+/C#': {
            'd': [(None, 6), (None, 4)],
            'A': [(None, 6), (NATURAL, 4)],
        },
        'D7': {
            'C': [(None, 7), (None, 5), (SHARP, 3)],
            'D': [(NATURAL, 7)],
            'G': [(None, 7)],
        },
        'Gm7/Bb': {
            'Eb': [(None, 6), (None, 5)],
            'f': [(None, 6), (None, 5), (NATURAL, 3)],
            'A': [(NATURAL, 6), (NATURAL, 5)],
        },
        'AM7/E': {
            'C lydian': [(SHARP, 6), (None, 4), (SHARP, 3)],
            'D': [(None, 4), (SHARP, 3)],
            'E': [(None, 4), (None, 3)],
        },
        'C#m7/B': {
            'D': [(SHARP, 6), (None, 4), (None, 2)],
            'A': [(None, 4), (None, 2)],
        },
    }

    for c, cases in chords.items():
        chord = Chord(c)
        for k, figures in cases.items():
            key = Key(k)
            assert chord.figures(key) == figures
