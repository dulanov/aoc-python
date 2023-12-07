from __future__ import annotations
import collections
from enum import Enum, auto
from typing import Iterable, Iterator
import doctest

day = "07"

example1 = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

example2 = example1


class HandType(Enum):
    FIVE_KIND = auto()
    FOUR_KIND = auto()
    FULL_HOUSE = auto()
    THREE_KIND = auto()
    TWO_PAIR = auto()
    ONE_PAIR = auto()
    HIGH_CARD = auto()

    def __lt__(self, other):
        return self.value < other.value

    @classmethod
    def from_str(cls, s: str) -> HandType:
        """Return the hand type from a string.

        >>> HandType.from_str("AAAAA")
        <HandType.FIVE_KIND: 1>

        >>> HandType.from_str("AA8AA")
        <HandType.FOUR_KIND: 2>

        >>> HandType.from_str("23332")
        <HandType.FULL_HOUSE: 3>

        >>> HandType.from_str("TTT98")
        <HandType.THREE_KIND: 4>

        >>> HandType.from_str("23432")
        <HandType.TWO_PAIR: 5>

        >>> HandType.from_str("A23A4")
        <HandType.ONE_PAIR: 6>

        >>> HandType.from_str("A2345")
        <HandType.HIGH_CARD: 7>
        """
        assert len(s) == 5
        match collections.Counter(s).most_common():
            case [(_, 5)]:
                return cls.FIVE_KIND
            case [(_, 4), (_, 1)]:
                return cls.FOUR_KIND
            case [(_, 3), (_, 2)]:
                return cls.FULL_HOUSE
            case [(_, 3), (_, 1), (_, 1)]:
                return cls.THREE_KIND
            case [(_, 2), (_, 2), (_, 1)]:
                return cls.TWO_PAIR
            case [(_, 2), (_, 1), (_, 1), (_, 1)]:
                return cls.ONE_PAIR
            case [(_, 1), (_, 1), (_, 1), (_, 1), (_, 1)]:
                return cls.HIGH_CARD


def part_one(puzzle: Iterable[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> import pprint
    >>> pprint.pprint(part_one(example1.splitlines()))
    [(<HandType.ONE_PAIR: 6>, ('32T3K', 765)),
     (<HandType.TWO_PAIR: 5>, ('KTJJT', 220)),
     (<HandType.TWO_PAIR: 5>, ('KK677', 28)),
     (<HandType.THREE_KIND: 4>, ('T55J5', 684)),
     (<HandType.THREE_KIND: 4>, ('QQQJA', 483))]

    >>> sum(map(lambda t: t[0] * t[1][1][1], enumerate(part_one(example1.splitlines()), start=1)))
    6440

    >>> sum(map(lambda t: t[0] * t[1][1][1], enumerate(part_one(open(f"2023/day{day}.in").readlines()), start=1)))
    248422077
    """
    result = []
    for hand in scan(puzzle):
        result.append((HandType.from_str(hand[0]), hand))
    conv = {c: f"{i:x}" for i, c in enumerate("AKQJT98765432")}
    return sorted(result, key=lambda t: (t[0], str2int(t[1][0], conv)), reverse=True)


def part_two(puzzle: Iterable[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> import pprint
    >>> pprint.pprint(part_two(example1.splitlines()))
    [(<HandType.ONE_PAIR: 6>, ('32T3K', 765)),
     (<HandType.TWO_PAIR: 5>, ('KK677', 28)),
     (<HandType.FOUR_KIND: 2>, ('T55J5', 684)),
     (<HandType.FOUR_KIND: 2>, ('QQQJA', 483)),
     (<HandType.FOUR_KIND: 2>, ('KTJJT', 220))]

    >>> sum(map(lambda t: t[0] * t[1][1][1], enumerate(part_two(example2.splitlines()), start=1)))
    5905

    >>> sum(map(lambda t: t[0] * t[1][1][1], enumerate(part_two(open(f"2023/day{day}.in").readlines()), start=1)))
    249817836
    """
    result = []
    for hand in scan(puzzle):
        result.append((HandType.from_str(opt(hand[0])), hand))
    conv = {c: f"{i:x}" for i, c in enumerate("AKQT98765432J")}
    return sorted(result, key=lambda t: (t[0], str2int(t[1][0], conv)), reverse=True)


def opt(hand: str) -> str:
    c = collections.Counter(hand.replace("J", ""))
    return hand.replace("J", c.most_common()[0][0] if c else "J")


def str2int(s: str, conv: map[str, str]) -> int:
    return int("".join([conv[c] for c in s]), 16)


def scan(puzzle: Iterable[str]) -> Iterator[tuple[int, str]]:
    for line in puzzle:
        els = line.split()
        yield els[0], int(els[1])


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
