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

example2 = example11


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
    [<Dir.E: 2>,
     <Dir.S: 3>,
     <Dir.S: 3>,
     <Dir.W: 4>,
     <Dir.W: 4>,
     <Dir.N: 1>,
     <Dir.N: 1>]

    >>> (len(part_one(example11.splitlines())) + 1) // 2
    4

    >>> pprint.pprint(part_one(example12.splitlines()))
    [<Dir.N: 1>,
     <Dir.E: 2>,
     <Dir.N: 1>,
     <Dir.E: 2>,
     <Dir.S: 3>,
     <Dir.S: 3>,
     <Dir.E: 2>,
     <Dir.S: 3>,
     <Dir.W: 4>,
     <Dir.W: 4>,
     <Dir.W: 4>,
     <Dir.S: 3>,
     <Dir.W: 4>,
     <Dir.N: 1>,
     <Dir.N: 1>]

    >>> (len(part_one(example12.splitlines())) + 1) // 2
    8

    >>> (len(part_one(open(f"2023/day{day}.in").readlines())) + 1) // 2
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

    >>> part_two(example2.splitlines())
    []

    >>> len(part_two(example2.splitlines()))
    0

    >> len(part_two(open(f"2023/day{day}.in").readlines()))
    ???
    """
    return []


def iter(grid: list[list[Tile]], x: int, y: int, d: Dir) -> Iterator[Dir]:
    while True:
        dx, dy = d.dlt()
        x, y = x + dx, y + dy
        if grid[y][x] == Tile.STRT:
            break
        d = grid[y][x].other(d)
        yield d


def scan(puzzle: Iterable[str]) -> Iterator[list[Tile]]:
    for line in puzzle:
        yield list(map(Tile.from_str, line))


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
