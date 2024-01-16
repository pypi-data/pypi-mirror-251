__all__ = ['Quality', 'Chord']

from dataclasses import dataclass
from enum import Enum
from typing import overload

from fugo import Accidental, Interval, Key, LetterName, NoteName


class Quality(list[Interval], Enum):
    intervals = lambda s: [Interval(i) for i in s.split()]
    # fmt: off
    MAJOR      = intervals('P1 M3 P5')
    MINOR      = intervals('P1 m3 P5')
    DIMINISHED = intervals('P1 m3 d5')
    AUGMENTED  = intervals('P1 M3 A5')

    MAJ_MIN_7  = intervals('P1 M3 P5 m7')
    MAJ_7      = intervals('P1 M3 P5 M7')
    MIN_7      = intervals('P1 m3 P5 m7')
    MIN_MAJ_7  = intervals('P1 m3 P5 M7')
    DIM_7      = intervals('P1 m3 d5 d7')
    HALF_DIM_7 = intervals('P1 m3 d5 m7')
    # fmt: on
    del intervals

    @classmethod
    def from_string(cls, /, symbol: str):
        mapping = {
            'M': cls.MAJOR,
            'maj': cls.MAJOR,
            '': cls.MAJOR,
            'm': cls.MINOR,
            'min': cls.MINOR,
            '-': cls.MINOR,
            'dim': cls.DIMINISHED,
            'º': cls.DIMINISHED,
            'o': cls.DIMINISHED,
            'aug': cls.AUGMENTED,
            '+': cls.AUGMENTED,
            '7': cls.MAJ_MIN_7,
            'Mm7': cls.MAJ_MIN_7,
            'maj7': cls.MAJ_7,
            'M7': cls.MAJ_7,
            'Δ': cls.MAJ_7,
            'Δ7': cls.MAJ_7,
            'min7': cls.MIN_7,
            'm7': cls.MIN_7,
            '-7': cls.MIN_7,
            'mM7': cls.MIN_MAJ_7,
            '-M7': cls.MIN_MAJ_7,
            '-Δ7': cls.MIN_MAJ_7,
            'minmaj7': cls.MIN_MAJ_7,
            'o7': cls.DIM_7,
            'º7': cls.DIM_7,
            'dim7': cls.DIM_7,
            'ø': cls.HALF_DIM_7,
            'ø7': cls.HALF_DIM_7,
            'm7b5': cls.HALF_DIM_7,
            'm7♭5': cls.HALF_DIM_7,
            'min7b5': cls.HALF_DIM_7,
            'min7♭5': cls.HALF_DIM_7,
        }

        try:
            return mapping[symbol.strip()]
        except KeyError:
            raise ValueError(f'invalid symbol: {symbol!r}') from None


@dataclass
class Chord:
    root: NoteName
    quality: list[Interval]
    inversion: int = 0

    @overload
    def __init__(self, chord: str, /):
        ...

    @overload
    def __init__(self, root: NoteName, quality: list[Interval], inversion: int = 0, /):
        ...

    def __init__(self, *args):
        match args:
            case str(),:
                copy = self.from_string(*args)
            case _:
                copy = self.from_attrs(*args)

        vars(self).update(vars(copy))

    def __iter__(self):
        return iter(self.note_names)

    def __len__(self):
        return len(self.note_names)

    def __hash__(self):
        return 0

    @classmethod
    def from_string(cls, name: str):
        rest = name.strip()

        _letter, rest = rest[0], rest[1:]
        letter = LetterName.from_string(_letter)

        if rest[:2] == 'bb':
            accidental = Accidental.DOUBLE_FLAT
            rest = rest[2:]
        else:
            try:
                accidental = Accidental.from_string(rest[0])
            except (ValueError, IndexError):
                accidental = Accidental.NATURAL
            else:
                rest = rest[1:]

        root = NoteName.from_attrs(letter, accidental)

        _quality, slash, _bass = rest.partition('/')

        if _quality:
            quality = Quality.from_string(_quality)
        else:
            quality = Quality.MAJOR if _letter.isupper() else Quality.MINOR

        if slash:
            bass = NoteName(_bass)
            inversion = Chord.from_attrs(root, quality).note_names.index(bass)
        else:
            inversion = 0

        return cls.from_attrs(root, quality, inversion)

    @classmethod
    def from_attrs(cls, root: NoteName, quality: list[Interval], inversion: int = 0):
        if inversion >= len(quality):
            raise ValueError(
                f'invalid inversion: {inversion}'
                f' (chord only has {len(quality)} members)'
            )

        chord = super().__new__(cls)
        chord.root = root
        chord.quality = quality
        chord.inversion = inversion
        return chord

    @property
    def note_names(self) -> list[NoteName]:
        # Find the chord members.
        intervals = self.quality
        notes = [self.root + interval for interval in intervals]

        # Invert the chord as necessary.
        return notes[self.inversion :] + notes[: self.inversion]

    @property
    def bass(self) -> NoteName:
        interval = self.quality[self.inversion]
        return self.root + interval

    @property
    def intervals(self) -> list[Interval]:
        bass, *notes = self.note_names
        return [note - bass for note in notes]

    def figures(
        self, key: Key | None = None, *, shorthand: bool = True
    ) -> list[tuple[Accidental | None, int]]:
        """Return the figures for a chord.

        args:
            - `key`:
                - `Key` for determining accidentals, or
                - `None` to attach accidentals to all figures
            - `shorthand`: omit implied figures

        returns:
            - list of `figure`s
                - `figure`: `(symbol, number)`
                    - `symbol`: an `Accidental` if required by `key`,
                    `None` otherwise
                    - `number`: interval above bass

        notes:
            - `shorthand` has no effect if `key is None`

        examples:
            >>> from fugo import Chord, Key
            >>> D7 = Chord('D7')
            >>> D7.figures()
            [(Accidental.NATURAL, 7), (Accidental.NATURAL, 5), (Accidental.SHARP, 3)]
            >>> D7.figures(Key('G'))
            [(None, 7)]
            >>> D7.figures(Key('G'), shorthand=False)
            [(None, 7), (None, 5), (None, 3)]
        """
        intervals = reversed(self.intervals)
        *notes, bass = reversed(self.note_names)

        def figure(note: NoteName, interval: Interval) -> tuple[Accidental | None, int]:
            requires_accidental = key is None or note not in key
            symbol = note.accidental if requires_accidental else None
            number = interval.size.number
            return symbol, number

        figures = [figure(note, interval) for note, interval in zip(notes, intervals)]

        if shorthand:
            match figures:
                # triad, root position (5/3 -> _)
                case [(None, 5), (None, 3)]:
                    figures = []

                # triad, 1st inversion (6/3 -> 6)
                case [(_, 6), (None, 3)]:
                    figures = figures[:1]

                # seventh, root position (7/5/3 -> 7)
                case [(_, 7), (None, 5), (None, 3)]:
                    figures = figures[:1]

                # seventh, 1st inversion (6/5/3 -> 6/5)
                case [(_, 6), (_, 5), (None, 3)]:
                    figures = figures[:2]

                # seventh, 2nd inversion (6/4/3 -> 4/3)
                case [(None, 6), (_, 4), (_, 3)]:
                    figures = figures[1:]

                # seventh, 3rd inversion (6/4/2 -> 4/2)
                case [(None, 6), (_, 4), (_, 2)]:
                    figures = figures[1:]

        return figures
