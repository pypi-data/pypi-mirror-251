__all__ = ['Mode', 'Degree', 'Key']

from dataclasses import dataclass
from enum import Enum, auto
from typing import overload

from fugo import Accidental, Interval, LetterName, NoteName


class Mode(Enum):
    parse = lambda s: tuple(Interval(i) for i in s.split())
    # fmt: off
    MAJOR = IONIAN  = parse('P1 M2 M3 P4 P5 M6 M7')
    DORIAN          = parse('P1 M2 m3 P4 P5 M6 m7')
    PHRYGIAN        = parse('P1 m2 m3 P4 P5 m6 m7')
    LYDIAN          = parse('P1 M2 M3 A4 P5 M6 M7')
    MIXOLYDIAN      = parse('P1 M2 M3 P4 P5 M6 m7')
    MINOR = AEOLIAN = parse('P1 M2 m3 P4 P5 m6 m7')
    LOCRIAN         = parse('P1 m2 m3 P4 d5 m6 m7')
    # fmt: on
    del parse

    @property
    def intervals(self) -> tuple[Interval, ...]:
        return self.value

    def __len__(self):
        return len(self.intervals)


class Degree(Enum):
    """Represent a scale degree."""

    # fmt: off
    TONIC        = auto()
    SUPERTONIC   = auto()
    MEDIANT      = auto()
    SUBDOMINANT  = auto()
    DOMINANT     = auto()
    SUBMEDIANT   = auto()
    LEADING_TONE = auto()
    SUBTONIC     = auto()
    SEVENTH      = auto()

    FIRST   = TONIC
    SECOND  = SUPERTONIC
    THIRD   = MEDIANT
    FOURTH  = SUBDOMINANT
    FIFTH   = DOMINANT
    SIXTH   = SUBMEDIANT
    # fmt: on

    @classmethod
    def _missing_(cls, degree: int):
        if degree < 1:
            raise ValueError(f'invalid scale degree ({degree!r})')

        i = degree - 1
        degrees = [
            cls.FIRST,
            cls.SECOND,
            cls.THIRD,
            cls.FOURTH,
            cls.FIFTH,
            cls.SIXTH,
            cls.SEVENTH,
        ]
        return degrees[i]


@dataclass
class Key:
    """Represent a key."""

    tonic: NoteName
    mode: Mode

    @overload
    def __init__(self, key: str, /):
        ...

    @overload
    def __init__(self, tonic: NoteName, mode: Mode, /):
        ...

    def __init__(self, *args):
        match args:
            case str(),:
                copy = self.from_string(*args)
            case NoteName(), Mode():
                copy = self.from_attrs(*args)
            case _:
                raise ValueError('invalid arguments')

        vars(self).update(vars(copy))

    def __iter__(self):
        return (self.tonic + interval for interval in self.mode.intervals)

    def __getitem__(self, degree: Degree) -> NoteName:
        notes = [*self]
        match degree:
            # fmt: off
            case Degree.TONIC:          return notes[0]
            case Degree.SUPERTONIC:     return notes[1]
            case Degree.MEDIANT:        return notes[2]
            case Degree.SUBDOMINANT:    return notes[3]
            case Degree.DOMINANT:       return notes[4]
            case Degree.SUBMEDIANT:     return notes[5]
            case Degree.SEVENTH:        return notes[6]
            case Degree.SUBTONIC:       return self.tonic - Interval('M2')
            case Degree.LEADING_TONE:   return self.tonic - Interval('m2')
            # fmt: on
            case _:
                raise ValueError(f'unrecognized scale degree {degree!r}')

    @classmethod
    def from_string(cls, name: str) -> 'Key':
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

        tonic = NoteName.from_attrs(letter, accidental)
        rest = rest.removeprefix('-').strip()

        match rest:
            case '':
                mode = Mode.MAJOR if _letter.isupper() else Mode.MINOR
            case 'M':
                mode = Mode.MAJOR
            case 'm':
                mode = Mode.MINOR
            case _:
                _mode = rest.upper()
                try:
                    mode = Mode[_mode]
                except KeyError:
                    raise ValueError(f'invalid mode {rest!r}') from None

        return cls.from_attrs(tonic, mode)

    @classmethod
    def from_attrs(cls, tonic: NoteName, mode: Mode) -> 'Key':
        key = super().__new__(cls)
        key.tonic = tonic
        key.mode = mode
        return key
