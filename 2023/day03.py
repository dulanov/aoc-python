from __future__ import annotations
from typing import Iterable, Iterator
import doctest
import re
import uuid

day = "03"

example1 = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

example2 = """\
"""


class Point:
    """A point in the grid."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: Point) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def adjacent(self, ln: int = 1) -> list[Point]:
        """Return the adjacent points."""
        points = [
            Point(self.x - 1, self.y - 1),
            Point(self.x - 1, self.y),
            Point(self.x - 1, self.y + 1),
            Point(self.x + ln, self.y - 1),
            Point(self.x + ln, self.y),
            Point(self.x + ln, self.y + 1),
        ]
        for i in range(ln):
            points.append(Point(self.x + i, self.y - 1))
            points.append(Point(self.x + i, self.y + 1))
        return points


def part_one(puzzle: Iterable[str]) -> tuple[list[int], list[int]]:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    ([35, 467, 592, 598, 617, 633, 664, 755], [58, 114])

    >>> sum(part_one(example1.splitlines())[0])
    4361

    >>> sum(part_one(open(f"2023/day{day}.in").readlines())[0])
    556367
    """
    input, adj, ndj = list(scan(puzzle)), [], []
    symbols = {p for p, s in input if not s[0].isdigit()}
    for p, s in input:
        if not s[0].isdigit():
            continue
        if any(p in symbols for p in p.adjacent(len(s))):
            adj.append(int(s))
        else:
            ndj.append(int(s))
    return sorted(adj), sorted(ndj)


def part_two(puzzle: Iterable[str]) -> list[tuple(int, int)]:
    """Solve part two of the puzzle.

    >>> part_two(example1.splitlines())
    [(35, 467), (598, 755)]

    >>> sum(map(lambda t: t[0] * t[1], part_two(example1.splitlines())))
    467835

    >>> sum(map(lambda t: t[0] * t[1], part_two(open(f"2023/day{day}.in").readlines())))
    89471771
    """
    input, gears, nums = list(scan(puzzle)), [], {}
    for p, s in input:
        if not s[0].isdigit():
            continue
        id = uuid.uuid4()
        for i in range(len(s)):
            nums[Point(p.x + i, p.y)] = id, int(s)
    for p, s in input:
        if s != "*":
            continue
        ns = {nums[p] for p in p.adjacent() if p in nums}
        if len(ns) == 2:
            gears.append(
                (min(ns, key=lambda t: t[1])[1], max(ns, key=lambda t: t[1])[1])
            )
    return gears


def scan(puzzle: Iterable[str]) -> Iterator[tuple[Point, str]]:
    r = re.compile(r"(?P<num>\d+)|(?P<sym>[^\.\d\n]+)")
    for y, line in enumerate(puzzle):
        for m in r.finditer(line):
            yield Point(m.start(), y), m.group()
    return []


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
