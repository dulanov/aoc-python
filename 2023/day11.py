from itertools import chain
import itertools
from typing import Iterable, Iterator
import doctest

day = "11"

example1 = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


example2 = example1


def part_one(puzzle: Iterable[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> len(part_one(example1.splitlines()))
    36

    >>> sum(part_one(example1.splitlines()))
    374

    >>> sum(part_one(open(f"2023/day{day}.in")))
    9233514
    """
    galaxies = set(chain.from_iterable(scan(puzzle)))
    xs, ys = {x for x, _ in galaxies}, {y for _, y in galaxies}
    for x in sorted(set(range(max(xs))) - xs, reverse=True):
        galaxies = {(g[0] + 1, g[1]) if g[0] > x else g for g in galaxies}
    for y in sorted(set(range(max(ys))) - ys, reverse=True):
        galaxies = {(g[0], g[1] + 1) if g[1] > y else g for g in galaxies}
    return [distance(a, b) for a, b in itertools.combinations(galaxies, 2)]


def part_two(puzzle: Iterable[str], factor: int = 1000000) -> list[int]:
    """Solve part two of the puzzle.

    >>> sum(part_two(example2.splitlines(), factor=10))
    1030

    >>> sum(part_two(example2.splitlines(), factor=100))
    8410

    >>> sum(part_two(open(f"2023/day{day}.in")))
    363293506944
    """
    galaxies = set(chain.from_iterable(scan(puzzle)))
    xs, ys = {x for x, _ in galaxies}, {y for _, y in galaxies}
    for x in sorted(set(range(max(xs))) - xs, reverse=True):
        galaxies = {(g[0] + factor - 1, g[1]) if g[0] > x else g for g in galaxies}
    for y in sorted(set(range(max(ys))) - ys, reverse=True):
        galaxies = {(g[0], g[1] + factor - 1) if g[1] > y else g for g in galaxies}
    return [distance(a, b) for a, b in itertools.combinations(galaxies, 2)]


def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Return the Manhattan distance between two points.

    >>> distance((1, 6), (5, 11))
    9
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def scan(puzzle: Iterable[str]) -> Iterator[list[tuple[int, int]]]:
    for y, line in enumerate(puzzle):
        yield [(x, y) for x, c in enumerate(line) if c == "#"]


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
