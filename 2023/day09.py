import doctest
import itertools
from typing import Iterator

day = "09"  # https://adventofcode.com/2023/day/9

example1 = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


example2 = example1


def part_one(puzzle: list[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    [(3, 18), (1, 7, 28), (2, 8, 23, 68)]

    >>> import operator
    >>> sum(map(operator.itemgetter(-1), part_one(example1.splitlines())))
    114

    >>> sum(map(operator.itemgetter(-1), part_one(open(f"2023/day{day}.in"))))
    1974232246
    """
    result = []
    for ns in scan(puzzle):
        lasts = []
        while any(ns):
            lasts.append(ns[-1])
            ns = [n2 - n1 for n1, n2 in itertools.pairwise(ns)]
        result.append(tuple(itertools.accumulate(reversed(lasts))))
    return result


def part_two(puzzle: list[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    [(3, -3), (1, 1, 0), (2, -2, 5, 5)]

    >>> import operator
    >>> sum(map(operator.itemgetter(-1), part_two(example2.splitlines())))
    2

    >>> sum(map(operator.itemgetter(-1), part_two(open(f"2023/day{day}.in"))))
    928
    """
    result = []
    for ns in scan(puzzle):
        lasts = []
        while any(ns):
            lasts.append(ns[0])
            ns = [n2 - n1 for n1, n2 in itertools.pairwise(ns)]
        result.append(tuple(itertools.accumulate(reversed(lasts), lambda a, b: b - a)))
    return result


def scan(puzzle: list[str]) -> Iterator[list[int]]:
    for line in puzzle:
        yield list(map(int, line.split()))


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
