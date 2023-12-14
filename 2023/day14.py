from enum import Enum
from typing import Iterable, Iterator
import bisect
import collections
import doctest
import itertools

day = "14"

example1 = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


example2 = example1


class Dir(Enum):
    N, E, S, W = range(4)


Pos = collections.namedtuple("Pos", "x y")

Grid = collections.namedtuple("Grid", "rock_xs rock_ys cube_xs cube_ys")


def part_one(puzzle: Iterable[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    [5, 2, 4, 3, 0, 0, 3, 1, 0, 0]

    >>> from itertools import starmap
    >>> from operator import mul
    >>> sum(starmap(mul, enumerate(reversed(part_one(example1.splitlines())), start=1)))
    136

    >>> sum(starmap(mul, enumerate(reversed(part_one(open(f"2023/day{day}.in"))), start=1)))
    110090
    """
    g = Grid(
        collections.defaultdict(list),
        collections.defaultdict(list),
        collections.defaultdict(list),
        collections.defaultdict(list),
    )
    for size, (cube_shaped, rounded) in scan(puzzle):
        for r in cube_shaped:
            g.rock_xs[r.x].append(r)
            g.rock_ys[r.y].append(r)
        for r in rounded:
            g.cube_xs[r.x].append(r)
            g.cube_ys[r.y].append(r)
    tilt(g, size)
    return [len(g.cube_ys[y]) for y in range(1, size - 1)]


def part_two(puzzle: Iterable[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    []

    >>> sum(part_two(example2.splitlines()))
    0

    >> sum(part_two(open(f"2023/day{day}.in")))
    ???
    """
    return []


def tilt(g: Grid, n: int, /, *, d: Dir = Dir.N) -> None:
    for x in range(1, n - 1):
        cubes, new_cubes, lo = g.cube_xs[x], [], 0
        for r1, r2 in itertools.pairwise(g.rock_xs[x]):
            lo = bisect.bisect_left(cubes, r1, lo)
            lo = bisect.bisect_left(cubes, r2, lo)
            new_cubes += [Pos(r1.x, r1.y + i + 1) for i in range(lo - i)]
        g.cube_xs[x] = new_cubes
    g.cube_ys.clear()
    for r in itertools.chain.from_iterable(g.cube_xs.values()):
        g.cube_ys[r.y].append(r)
    return d


def scan(puzzle: Iterable[str]) -> Iterator[tuple[int, tuple[list[Pos], list[Pos]]]]:
    for y, line in enumerate(puzzle, start=1):
        line, size = "#" + line.strip() + "#", len(line.strip()) + 2
        if y == 1:
            yield size, ([Pos(x, 0) for x in range(size)], [])
        rounded = [Pos(x, y) for x, c in enumerate(line) if c == "O"]
        cube_shaped = [Pos(x, y) for x, c in enumerate(line) if c == "#"]
        yield size, (cube_shaped, rounded)
    yield size, ([Pos(x, size - 1) for x in range(size)], [])


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
