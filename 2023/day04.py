from typing import Iterable, Iterator
import doctest
import re

day = "04"

example1 = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

example2 = example1


def part_one(puzzle: Iterable[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    [8, 2, 2, 1, 0, 0]

    >>> sum(part_one(example1.splitlines()))
    13

    >>> sum(part_one(open(f"2023/day{day}.in").readlines()))
    25183
    """
    result = []
    for g1, g2 in scan(puzzle):
        if inter := set(g1).intersection(g2):
            result.append(2 ** (len(inter) - 1))
        else:
            result.append(0)
    return result


def part_two(puzzle: Iterable[str]) -> list[int]:
    """Solve part two of the puzzle.

    >> part_two(example2.splitlines())
    []

    >> sum(part_two(example2.splitlines()))
    0

    >> sum(part_two(open(f"2023/day{day}.in").readlines()))
    ???
    """
    return []


def scan(puzzle: Iterable[str]) -> Iterator[tuple[list[int], list[int]]]:
    r = re.compile(r"Card\s+\d+:(.*)\|(.*)")
    for line in puzzle:
        g1, g2 = r.match(line).groups()
        yield ([int(x) for x in g1.split()], [int(x) for x in g2.split()])


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
