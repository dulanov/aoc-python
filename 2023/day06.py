from typing import Iterable
import doctest
import math
import re

day = "06"

example1 = """\
Time:      7  15   30
Distance:  9  40  200
"""

example2 = example1


def part_one(puzzle: Iterable[str]) -> list[tuple[int, int]]:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    [(2, 6), (4, 12), (11, 20)]

    >>> import functools
    >>> import operator
    >>> functools.reduce(operator.mul, list(map(lambda t: t[1] - t[0], part_one(example1.splitlines()))))
    288

    >>> functools.reduce(operator.mul, list(map(lambda t: t[1] - t[0], part_one(open(f"2023/day{day}.in")))))
    220320
    """
    wins = []
    for race in scan(puzzle):
        wins.append(solve(*race))
    return wins


def part_two(puzzle: Iterable[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example1.splitlines())
    (14, 71517)

    >>> import functools
    >>> import operator
    >>> -functools.reduce(operator.sub, part_two(example1.splitlines()))
    71503

    >>> -functools.reduce(operator.sub, part_two(open(f"2023/day{day}.in")))
    34454850
    """
    return solve(*scan(puzzle, collapsed=True)[0])


def solve(t: int, d: int) -> tuple[int, int]:
    """Solve for t and d.

    >>> solve(7, 9)
    (2, 6)

    >>> solve(15, 40)
    (4, 12)

    >>> solve(30, 200)
    (11, 20)
    """
    n1 = math.ceil((t - math.sqrt(t**2 - 4 * (d + 1))) / 2)
    n2 = math.ceil((t + math.sqrt(t**2 - 4 * d)) / 2)
    return n1, n2


def scan(puzzle: Iterable[str], collapsed: bool = False) -> list[tuple[int, int]]:
    for line in puzzle:
        if line.startswith("Time:"):
            if collapsed:
                time = int("".join(re.findall(r"\d+", line)))
            else:
                times = list(map(int, re.findall(r"\d+", line)))
        elif line.startswith("Distance:"):
            if collapsed:
                distance = int("".join(re.findall(r"\d+", line)))
            else:
                distances = list(map(int, re.findall(r"\d+", line)))
    return [(time, distance)] if collapsed else list(zip(times, distances))


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
