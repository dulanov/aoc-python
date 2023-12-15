from enum import Enum
from itertools import pairwise
from typing import Iterator
import bisect
import collections
import doctest

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


def part_one(puzzle: Iterator[str]) -> list[int]:
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
    rocks, cubes = [], []
    for size, (cube_shaped, rounded) in scan(puzzle):
        if not rocks:
            for i in range(size):  # add border of rocks (`#`) around the grid
                rocks.extend((Pos(i, -1), Pos(-1, i), Pos(i, size), Pos(size, i)))
        rocks.extend(cube_shaped)
        cubes.extend(rounded)
    return list(map(len, iter(tilt(rocks, cubes, size), size)))


def part_two(puzzle: Iterator[str], circles: int = 1_000_000_000) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines(), circles=1)
    [0, 1, 2, 2, 3, 2, 1, 4, 1, 2]

    >>> part_two(example2.splitlines(), circles=2)
    [0, 1, 0, 1, 3, 2, 2, 3, 2, 4]

    >>> part_two(example2.splitlines(), circles=3)
    [0, 1, 0, 1, 3, 2, 2, 3, 2, 4]

    >>> from itertools import starmap
    >>> from operator import mul
    >>> sum(starmap(mul, enumerate(reversed(part_two(example2.splitlines())), start=1)))
    64

    >>> sum(starmap(mul, enumerate(reversed(part_two(open(f"2023/day{day}.in"))), start=1)))
    95254
    """
    rocks, cubes = [], []
    for size, (cube_shaped, rounded) in scan(puzzle):
        if not rocks:
            for i in range(size):  # add border of rocks (`#`) around the grid
                rocks.extend((Pos(i, -1), Pos(-1, i), Pos(i, size), Pos(size, i)))
        rocks.extend(cube_shaped)
        cubes.extend(rounded)
    loop_detector = {}
    while circles > 0:
        for dir in [Dir.N, Dir.W, Dir.S, Dir.E]:
            cubes = tilt(rocks, cubes, size, dir=dir)
        circles, hsh = circles - 1, hash(tuple(cubes))
        if hsh in loop_detector:
            circles %= loop_detector[hsh] - circles
        loop_detector[hsh] = circles
    return list(map(len, iter(cubes, size)))


def tilt(rs: list[Pos], cs: list[Pos], n: int, /, *, dir: Dir = Dir.N) -> list[Pos]:
    vert, rev = dir in (Dir.N, Dir.S), dir in (Dir.S, Dir.E)
    new_cubes, delta = [], (0, 1) if vert else (1, 0)
    for rs, cs in zip(map(pairwise, iter(rs, n, vert=vert)), iter(cs, n, vert=vert)):
        for r1, r2 in rs:
            m = bisect.bisect(cs, r2) - bisect.bisect(cs, r1)
            r, d = (r1, delta) if not rev else (r2, (-delta[0], -delta[1]))
            new_cubes += [Pos(r.x + i * d[0], r.y + i * d[1]) for i in range(1, m + 1)]
    return new_cubes


def iter(l: list[Pos], n: int, /, *, vert: bool = False) -> Iterator[list[Pos]]:
    l, lo = sorted(l, key=lambda p: (p.x, p.y) if vert else (p.y, p.x)), 0
    for i in range(-1, n):
        hi = bisect.bisect(l, i, lo, key=lambda p: p.x if vert else p.y)
        if i != -1:  # skip the border of rocks (`#`)
            yield l[lo:hi]
        lo = hi


def scan(puzzle: Iterator[str]) -> Iterator[tuple[int, tuple[list[Pos], list[Pos]]]]:
    for y, line in enumerate(puzzle):
        rounded = [Pos(x, y) for x, c in enumerate(line.strip()) if c == "O"]
        cube_shaped = [Pos(x, y) for x, c in enumerate(line.strip()) if c == "#"]
        yield len(line.strip()), (cube_shaped, rounded)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
