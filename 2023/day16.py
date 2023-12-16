from __future__ import annotations
import collections
from enum import Enum
import functools
import itertools
from typing import Iterator
import doctest

day = "16"

example1 = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""


example2 = example1


Beam = collections.namedtuple("Beam", "x y d")


class Dir(Enum):
    U, D, L, R = range(4)

    @functools.cache
    def nex_pos(self, x: int, y: int) -> tuple[int, int]:
        return (
            x + (self == Dir.R) - (self == Dir.L),
            y + (self == Dir.D) - (self == Dir.U),
        )


class Type(Enum):
    EMPTY = "."
    MIRROR = "/"
    MIRROR_BACKSLASH = "\\"
    SPLITTER_HORIZONTAL = "-"
    SPLITTER_VERTICAL = "|"

    def __repr__(self) -> str:
        return self.value

    @functools.cache
    def dir_to_flag(self, d: Dir) -> int:
        match self:
            case Type.EMPTY:
                return 1 if d in (Dir.U, Dir.D) else 2
            case Type.MIRROR:
                return 1 if d in (Dir.U, Dir.L) else 2
            case Type.MIRROR_BACKSLASH:
                return 1 if d in (Dir.U, Dir.R) else 2
            case Type.SPLITTER_HORIZONTAL | Type.SPLITTER_VERTICAL:
                return 3

    @functools.cache
    def process_beam(self, d: Dir) -> tuple[int, list[Dir]]:
        if self == Type.EMPTY:
            return self.dir_to_flag(d), [d]

        if self == Type.MIRROR:
            return self.dir_to_flag(d), [(Dir.R, Dir.L, Dir.D, Dir.U)[d.value]]

        if self == Type.MIRROR_BACKSLASH:
            return self.dir_to_flag(d), [(Dir.L, Dir.R, Dir.U, Dir.D)[d.value]]

        if self == Type.SPLITTER_HORIZONTAL:
            return 3, ([Dir.L, Dir.R], [Dir.L, Dir.R], [Dir.L], [Dir.R])[d.value]

        if self == Type.SPLITTER_VERTICAL:
            return 3, ([Dir.U], [Dir.D], [Dir.U, Dir.D], [Dir.U, Dir.D])[d.value]

    def visited(self, f: int, d: Dir) -> bool:
        return self.dir_to_flag(d) & f

    @classmethod
    def from_str(cls, s: str) -> Type:
        return next(t for t in cls if s == t.value)


def part_one(puzzle: Iterator[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> print(part_one(example1.splitlines()))
    ######....
    .#...#....
    .#...#####
    .#...##...
    .#...##...
    .#...##...
    .#..####..
    ########..
    .#######..
    .#...#.#..

    >>> sum(c == "#" for l in part_one(example1.splitlines()) for c in l)
    46

    >>> sum(c == "#" for l in part_one(open(f"2023/day{day}.in")) for c in l)
    7860
    """
    grid = [tiles for tiles in scan(puzzle)]
    solve(grid, Beam(-1, 0, Dir.R))
    return diagram(grid)


def part_two(puzzle: Iterator[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    (51, Beam(x=3, y=-1, d=<Dir.D: 1>))

    >>> part_two(example2.splitlines())[0]
    51

    >>> part_two(open(f"2023/day{day}.in"))[0]
    8331
    """
    grid, res = [tiles for tiles in scan(puzzle)], (0, None)
    for (x, y), d, (dx, dy) in [
        ((0, -1), Dir.D, (1, 0)),
        ((-1, 0), Dir.R, (0, 1)),
        ((0, len(grid)), Dir.U, (1, 0)),
        ((len(grid), 0), Dir.L, (0, 1)),
    ]:
        for i in range(len(grid)):
            for j, k in itertools.product(range(len(grid[0])), range(len(grid))):
                grid[k][j] = grid[k][j][0], 0
            beam = Beam(x + i * dx, y + i * dy, d)
            solve(grid, beam)
            if (v := energized_tiles(grid)) > res[0]:
                res = (v, beam)
    return res


def solve(grid: list[list[tuple[Type, int]]], beam: Beam) -> None:
    stack = collections.deque([beam])
    while stack:
        beam = stack.pop()
        x, y = beam.d.nex_pos(beam.x, beam.y)
        if not (0 <= x < len(grid[0]) and 0 <= y < len(grid)):
            continue
        tile = grid[y][x]
        if tile[0].visited(tile[1], beam.d):
            continue
        f, dirs = tile[0].process_beam(beam.d)
        grid[y][x] = tile[0], tile[1] | f
        stack.extend(Beam(x, y, d) for d in dirs)
    return grid


def diagram(grid: list[list[tuple[Type, int]]]) -> str:
    result = []
    for tiles in grid:
        result.append("".join(map(lambda t: "#" if t[1] != 0 else ".", tiles)))
    return "\n".join(result)


def energized_tiles(grid: list[list[tuple[Type, int]]]) -> int:
    return sum(sum(t[1] != 0 for t in tiles) for tiles in grid)


def scan(puzzle: Iterator[str]) -> Iterator[list[tuple[Type, int]]]:
    for line in puzzle:
        if not (line := line.strip("\n")):
            continue
        yield [(Type.from_str(c), 0) for c in line]


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
