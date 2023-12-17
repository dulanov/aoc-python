from enum import Enum
from itertools import pairwise
from typing import Iterator
import bisect
import collections
import doctest
import functools

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
    rocks = iter(rocks, size, vert=True)
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
    loop_hash, vrocks, hrocks = {}, iter(rocks, size, vert=True), iter(rocks, size)
    while circles > 0:
        for dir, rocks in [
            (Dir.N, vrocks),
            (Dir.W, hrocks),
            (Dir.S, vrocks),
            (Dir.E, hrocks),
        ]:
            cubes = tilt(rocks, cubes, size, dir)
        circles, hsh = circles - 1, hash(tuple(cubes))
        if hsh in loop_hash:
            circles %= loop_hash[hsh] - circles
        loop_hash[hsh] = circles
    return list(map(len, iter(cubes, size)))


def tilt(rs: list[list[Pos]], cs: list[Pos], n: int, d: Dir = Dir.N) -> list[Pos]:
    new_cubes, vert, rev = [], d in (Dir.N, Dir.S), d in (Dir.S, Dir.E)
    for rs, cs in zip(map(pairwise, rs), iter(cs, n, vert=vert)):
        lo = None
        for r1, r2 in rs:
            if lo is None:
                lo = bisect.bisect(cs, r1)
            lo, prev = bisect.bisect(cs, r2, lo), lo
            new_cubes.extend(cubes(r1, r2, lo - prev, vert=vert, rev=rev))
    return new_cubes


def iter(l: list[Pos], n: int, /, *, vert: bool = False) -> list[list[Pos]]:
    l, ls, lo = sorted(l, key=lambda p: (p.x, p.y) if vert else (p.y, p.x)), [], 0
    for i in range(-1, n):
        hi = bisect.bisect(l, i, lo, key=lambda p: p.x if vert else p.y)
        if i != -1:  # skip the border of rocks (`#`)
            ls.append(l[lo:hi])
        lo = hi
    return ls


@functools.cache
def cubes(
    p1: Pos, p2: Pos, n: int, /, *, vert: bool = False, rev: bool = False
) -> list[Pos]:
    delta = (0, 1) if vert else (1, 0)
    p, delta = (p1, delta) if not rev else (p2, (-delta[0], -delta[1]))
    return [Pos(p.x + i * delta[0], p.y + i * delta[1]) for i in range(1, n + 1)]


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
