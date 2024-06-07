from __future__ import annotations

import doctest
import operator
from enum import Enum
from typing import Iterator

day = "18"  # https://adventofcode.com/2023/day/18

example1 = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""


example2 = example1


class Dir(Enum):
    R, D, L, U = range(4)

    def next_pos(self, x: int, y: int, n: int = 1) -> tuple[int, int]:
        return (
            x + n * ((self == Dir.R) - (self == Dir.L)),
            y + n * ((self == Dir.D) - (self == Dir.U)),
        )


def part_one(puzzle: list[str]) -> tuple[int, int]:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    (24, 38)

    >>> sum(part_one(example1.splitlines()))
    62

    >>> sum(part_one(open(f"2023/day{day}.in")))
    50603
    """
    return solve(map(operator.itemgetter(0), scan(puzzle)))


def part_two(puzzle: list[str]) -> tuple[int, int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    (952401738853, 6405262)

    >>> sum(part_two(example2.splitlines()))
    952408144115

    >>> sum(part_two(open(f"2023/day{day}.in")))
    96556251590677
    """
    return solve(map(operator.itemgetter(1), scan(puzzle)))


def solve(plan: map[tuple[Dir, int]]) -> tuple[int, int]:
    # https://en.wikipedia.org/wiki/Pick's_theorem
    # https://en.wikipedia.org/wiki/Shoelace_formula
    x, y, a, b = 0, 0, 0, 0
    for d, l in plan:
        dx, dy = d.next_pos(0, 0, l)
        x, y = x + dx, y + dy
        a, b = a + x * dy, b + l
    return a - b // 2 + 1, b


def scan(puzzle: list[str]) -> Iterator[tuple[tuple[Dir, int], tuple[Dir, int]]]:
    for line in puzzle:
        entries = line.strip("\n").split()
        yield (Dir[entries[0]], int(entries[1])), (
            Dir(int(entries[2][7])),
            int(entries[2][2:7], 16),
        )


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
