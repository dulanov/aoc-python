from typing import Iterable, Tuple
import doctest


day = "01"

example = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""


def part_one(puzzle: Iterable[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> part_one(example.splitlines())
    [12, 38, 15, 77]

    >>> sum(part_one(example.splitlines()))
    142

    >>> sum(part_one(open(f"2023/day{day}.in")))
    55130
    """
    return [t[0] * 10 + t[-1] for t in scan(puzzle)]


def scan(puzzle: Iterable[str]) -> Iterable[Tuple[int, ...]]:
    for line in puzzle:
        digits = [c for c in line if c.isdigit()]
        yield tuple(map(int, digits))


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
