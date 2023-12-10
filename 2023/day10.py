from __future__ import annotations
from enum import Enum, auto
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
    N = auto()
    E = auto()
    S = auto()
    W = auto()

    def dlt(self) -> tuple[int, int]:
        match self:
            case Dir.N:
                return (0, -1)
            case Dir.E:
                return (1, 0)
            case Dir.S:
                return (0, 1)
            case Dir.W:
                return (-1, 0)

    def inv(self) -> Dir:
        match self:
            case Dir.N:
                return Dir.S
            case Dir.E:
                return Dir.W
            case Dir.S:
                return Dir.N
            case Dir.W:
                return Dir.E


class Tile(Enum):
    NSPIPE = auto()
    WEPIPE = auto()
    NEPIPE = auto()
    NWPIPE = auto()
    WSPIPE = auto()
    ESPIPE = auto()
    STRT = auto()
    GND = auto()

    def dirs(self) -> tuple(Dir, Dir):
        match self:
            case Tile.NSPIPE:
                return (Dir.N, Dir.S)
            case Tile.WEPIPE:
                return (Dir.W, Dir.E)
            case Tile.NEPIPE:
                return (Dir.N, Dir.E)
            case Tile.NWPIPE:
                return (Dir.N, Dir.W)
            case Tile.WSPIPE:
                return (Dir.W, Dir.S)
            case Tile.ESPIPE:
                return (Dir.E, Dir.S)
        raise ValueError(f"{self} not supported")

    def other(self, d: Dir) -> Dir:
        d1, d2 = self.dirs()
        if d.inv() != d1 and d.inv() != d2:
            raise ValueError(f"{d} not supported by {self}")
        return d1 if d.inv() == d2 else d2

    @classmethod
    def from_str(cls, s: str) -> Tile:
        match s:
            case "|":
                return Tile.NSPIPE
            case "-":
                return Tile.WEPIPE
            case "L":
                return Tile.NEPIPE
            case "J":
                return Tile.NWPIPE
            case "7":
                return Tile.WSPIPE
            case "F":
                return Tile.ESPIPE
            case "S":
                return Tile.STRT
            case ".":
                return Tile.GND


def part_one(puzzle: Iterable[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> import pprint
    >>> pprint.pprint(part_one(example11.splitlines()))
    [(1, 1, <Dir.E: 2>),
     (2, 1, <Dir.E: 2>),
     (3, 1, <Dir.S: 3>),
     (3, 2, <Dir.S: 3>),
     (3, 3, <Dir.W: 4>),
     (2, 3, <Dir.W: 4>),
     (1, 3, <Dir.N: 1>),
     (1, 2, <Dir.N: 1>)]

    >>> len(part_one(example11.splitlines())) // 2
    4

    >>> pprint.pprint(part_one(example12.splitlines()))
    [(0, 2, <Dir.E: 2>),
     (1, 2, <Dir.N: 1>),
     (1, 1, <Dir.E: 2>),
     (2, 1, <Dir.N: 1>),
     (2, 0, <Dir.E: 2>),
     (3, 0, <Dir.S: 3>),
     (3, 1, <Dir.S: 3>),
     (3, 2, <Dir.E: 2>),
     (4, 2, <Dir.S: 3>),
     (4, 3, <Dir.W: 4>),
     (3, 3, <Dir.W: 4>),
     (2, 3, <Dir.W: 4>),
     (1, 3, <Dir.S: 3>),
     (1, 4, <Dir.W: 4>),
     (0, 4, <Dir.N: 1>),
     (0, 3, <Dir.N: 1>)]

    >>> len(part_one(example12.splitlines())) // 2
    8

    >>> len(part_one(open(f"2023/day{day}.in").readlines())) // 2
    6599
    """
    grid, x, y = [], 0, 0
    for i, tiles in enumerate(scan(puzzle)):
        if Tile.STRT in tiles:
            x, y = tiles.index(Tile.STRT), i
        grid.append(tiles)
    for d in [Dir.N, Dir.E, Dir.S, Dir.W]:
        try:
            dx, dy = d.dlt()
            grid[y + dy][x + dx].other(d)
        except ValueError:
            continue
        else:
            break
    return list(iter(grid, x, y, d))


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

    >>> len(part_two(open(f"2023/day{day}.in").readlines()))
    477
    """
    grid, x, y = [], 0, 0
    for i, tiles in enumerate(scan(puzzle)):
        if Tile.STRT in tiles:
            x, y = tiles.index(Tile.STRT), i
        grid.append(tiles)
    for d in [Dir.N, Dir.E, Dir.S, Dir.W]:
        try:
            dx, dy = d.dlt()
            grid[y + dy][x + dx].other(d)
        except ValueError:
            continue
        else:
            break
    enclosed_tiles = []
    loop = {(x, y): d for x, y, d in iter(grid, x, y, d)}
    for y in range(len(grid)):
        winding_number = 0  # https://en.wikipedia.org/wiki/Nonzero-rule
        for x in range(len(grid[y])):
            if (x, y) in loop and (x, y + 1) in loop:
                if loop[x, y + 1] == Dir.N:
                    winding_number += 1
                elif loop[x, y] == Dir.S:
                    winding_number -= 1
            if (x, y) not in loop and winding_number != 0:
                enclosed_tiles.append((x, y))
    return enclosed_tiles


def iter(
    grid: list[list[Tile]], x: int, y: int, d: Dir
) -> Iterator[tuple[int, int, Dir]]:
    while True:
        yield x, y, d
        dx, dy = d.dlt()
        x, y = x + dx, y + dy
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
