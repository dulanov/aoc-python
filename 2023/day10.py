from __future__ import annotations
from enum import Enum
from typing import Iterable, Iterator
import doctest

day = "10"

example11 = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""


example12 = """\
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

example21 = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

example22 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

example23 = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""


class Dir(Enum):
    N, E, S, W = ((0, -1), "S"), ((1, 0), "W"), ((0, 1), "N"), ((-1, 0), "E")

    def __call__(self, x: int, y: int) -> tuple[int, int]:
        dx, dy = self.value[0]
        return x + dx, y + dy

    def __repr__(self) -> str:
        return self.name

    def inv(self) -> Dir:
        return Dir[self.value[1]]


class Tile(Enum):
    NSPIPE = ("|", Dir.N, Dir.S)
    WEPIPE = ("-", Dir.W, Dir.E)
    NEPIPE = ("L", Dir.N, Dir.E)
    NWPIPE = ("J", Dir.N, Dir.W)
    WSPIPE = ("7", Dir.W, Dir.S)
    ESPIPE = ("F", Dir.E, Dir.S)
    STRT = ("S", None, None)
    GND = (".", None, None)

    def other(self, d: Dir) -> Dir:
        d1, d2 = self.value[1], self.value[2]
        if d.inv() != d1 and d.inv() != d2:
            raise ValueError(f"{d} not supported by {self}")
        return d1 if d.inv() == d2 else d2

    @classmethod
    def from_str(cls, s: str) -> Tile:
        return next(t for t in cls if s == t.value[0])


def part_one(puzzle: Iterable[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> import pprint
    >>> pprint.pprint(part_one(example11.splitlines()))
    [(1, 1, E),
     (2, 1, E),
     (3, 1, S),
     (3, 2, S),
     (3, 3, W),
     (2, 3, W),
     (1, 3, N),
     (1, 2, N)]

    >>> len(part_one(example11.splitlines())) // 2
    4

    >>> pprint.pprint(part_one(example12.splitlines()))
    [(0, 2, E),
     (1, 2, N),
     (1, 1, E),
     (2, 1, N),
     (2, 0, E),
     (3, 0, S),
     (3, 1, S),
     (3, 2, E),
     (4, 2, S),
     (4, 3, W),
     (3, 3, W),
     (2, 3, W),
     (1, 3, S),
     (1, 4, W),
     (0, 4, N),
     (0, 3, N)]

    >>> len(part_one(example12.splitlines())) // 2
    8

    >>> len(part_one(open(f"2023/day{day}.in"))) // 2
    6599
    """
    grid = []
    for i, tiles in enumerate(scan(puzzle)):
        if Tile.STRT in tiles:
            sx, sy = tiles.index(Tile.STRT), i
        grid.append(tiles)
    for d in [Dir.N, Dir.E, Dir.S, Dir.W]:
        try:
            x, y = d(sx, sy)
            grid[y][x].other(d)
        except ValueError:
            continue
        else:
            break
    return list(iter(grid, sx, sy, d))


def part_two(puzzle: Iterable[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example21.splitlines())
    [(2, 6), (3, 6), (7, 6), (8, 6)]

    >>> len(part_two(example21.splitlines()))
    4

    >>> part_two(example22.splitlines())
    [(14, 3), (7, 4), (8, 4), (9, 4), (7, 5), (8, 5), (6, 6), (14, 6)]

    >>> len(part_two(example22.splitlines()))
    8

    >>> part_two(example23.splitlines())
    [(14, 3), (10, 4), (11, 4), (12, 4), (13, 4), (11, 5), (12, 5), (13, 5), (13, 6), (14, 6)]

    >>> len(part_two(example23.splitlines()))
    10

    >>> len(part_two(open(f"2023/day{day}.in")))
    477
    """
    grid = []
    for i, tiles in enumerate(scan(puzzle)):
        if Tile.STRT in tiles:
            sx, sy = tiles.index(Tile.STRT), i
        grid.append(tiles)
    for d in [Dir.N, Dir.E, Dir.S, Dir.W]:
        try:
            x, y = d(sx, sy)
            grid[y][x].other(d)
        except ValueError:
            continue
        else:
            break
    enclosed, loop = [], {(x, y): d for x, y, d in iter(grid, sx, sy, d)}
    for y in range(len(grid)):
        winding = 0  # https://en.wikipedia.org/wiki/Nonzero-rule
        for x in range(len(grid[y])):
            if (x, y) in loop and (x, y + 1) in loop:
                if loop[x, y + 1] == Dir.N:
                    winding += 1
                elif loop[x, y] == Dir.S:
                    winding -= 1
            if (x, y) not in loop and winding:
                enclosed.append((x, y))
    return enclosed


def iter(
    grid: list[list[Tile]], x: int, y: int, d: Dir
) -> Iterator[tuple[int, int, Dir]]:
    while True:
        yield x, y, d
        x, y = d(x, y)
        if grid[y][x] == Tile.STRT:
            break
        d = grid[y][x].other(d)


def scan(puzzle: Iterable[str]) -> Iterator[list[Tile]]:
    for line in puzzle:
        yield list(map(Tile.from_str, line))


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
