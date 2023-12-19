from __future__ import annotations
from collections import deque, namedtuple
from enum import Enum
import functools
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


Beam = namedtuple("Beam", "x y d")


class Grid:
    def __init__(self, iter: Iterator[list[Type]]) -> None:
        self.grid = [tiles for tiles in iter]

    def __contains__(self, pos: tuple[int, int]) -> bool:
        return 0 <= pos[0] < len(self) and 0 <= pos[1] < len(self)

    def __getitem__(self, pos: tuple[int, int]) -> Type:
        return self.grid[pos[1]][pos[0]]

    def __iter__(self) -> Iterator[list[Type]]:
        return iter(self.grid)

    def __len__(self) -> int:
        return len(self.grid)

    @functools.cache
    def slide(self, x: int, y: int, d: Dir) -> int:
        if not (x, y) in self:
            return 0
        x2, y2 = x, y
        while (x2, y2) in self and self.grid[y2][x2].slide(d):
            x2, y2 = d.nex_pos(x2, y2)
        return abs(x2 - x) + abs(y2 - y)


class Dir(Enum):
    U, D, L, R = range(4)

    def nex_pos(self, x: int, y: int, n: int = 1) -> tuple[int, int]:
        return (
            x + n * ((self == Dir.R) - (self == Dir.L)),
            y + n * ((self == Dir.D) - (self == Dir.U)),
        )


class Type(Enum):
    EMPTY = "."
    MIRROR = "/"
    MIRROR_BACKSLASH = "\\"
    SPLITTER_HORIZONTAL = "-"
    SPLITTER_VERTICAL = "|"

    def __repr__(self) -> str:
        return self.value

    def beam(self, d: Dir) -> list[Dir]:
        if self == Type.EMPTY:
            return [d]

        if self == Type.MIRROR:
            return [(Dir.R, Dir.L, Dir.D, Dir.U)[d.value]]

        if self == Type.MIRROR_BACKSLASH:
            return [(Dir.L, Dir.R, Dir.U, Dir.D)[d.value]]

        if self == Type.SPLITTER_HORIZONTAL:
            return ([Dir.L, Dir.R], [Dir.L, Dir.R], [Dir.L], [Dir.R])[d.value]

        if self == Type.SPLITTER_VERTICAL:
            return ([Dir.U], [Dir.D], [Dir.U, Dir.D], [Dir.U, Dir.D])[d.value]

    def proj(self, d: Dir) -> tuple[bool, bool]:
        if self == Type.EMPTY:
            return (True, False) if d in (Dir.U, Dir.D) else (False, True)

        if self == Type.MIRROR:
            return (True, False) if d in (Dir.U, Dir.L) else (False, True)

        if self == Type.MIRROR_BACKSLASH:
            return (True, False) if d in (Dir.U, Dir.R) else (False, True)

        if self == Type.SPLITTER_HORIZONTAL:
            return (True, False) if d in (Dir.L, Dir.R) else (True, True)

        if self == self == Type.SPLITTER_VERTICAL:
            return (False, True) if d in (Dir.U, Dir.D) else (True, True)

    def slide(self, d: Dir) -> bool:
        if self == Type.EMPTY:
            return True

        if self == Type.MIRROR or self == Type.MIRROR_BACKSLASH:
            return False

        if self == Type.SPLITTER_HORIZONTAL:
            return d in (Dir.L, Dir.R)

        if self == self == Type.SPLITTER_VERTICAL:
            return d in (Dir.U, Dir.D)

    @classmethod
    def from_str(cls, s: str) -> Type:
        return next(t for t in cls if s == t.value)


def part_one(puzzle: Iterator[str]) -> str:
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
    result, grid = [], Grid(scan(puzzle))
    seen = solve(grid, Beam(-1, 0, Dir.R))
    for y in range(len(grid)):
        result.append("".join("#" if (x, y) in seen else "." for x in range(len(grid))))
    return "\n".join(result)


def part_two(puzzle: Iterator[str]) -> tuple(int, Beam):
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    (51, Beam(x=3, y=-1, d=<Dir.D: 1>))

    >>> part_two(example2.splitlines())[0]
    51

    >>> part_two(open(f"2023/day{day}.in"))[0]
    8331
    """
    grid, rs = Grid(scan(puzzle)), (0, None)
    for (x, y), (dx, dy), d in [
        ((0, -1), (1, 0), Dir.D),
        ((-1, 0), (0, 1), Dir.R),
        ((0, len(grid)), (1, 0), Dir.U),
        ((len(grid), 0), (0, 1), Dir.L),
    ]:
        for i in range(len(grid)):
            beam = Beam(x + i * dx, y + i * dy, d)
            if (v := len(solve(grid, beam))) > rs[0]:
                rs = (v, beam)
    return rs


def solve(grid: Grid, beam: Beam) -> set[complex]:
    seen, stack = (set(), set()), deque([beam])
    while stack:
        beam = stack.pop()
        x, y = beam.d.nex_pos(beam.x, beam.y)
        if n := grid.slide(x, y, beam.d):  # sliding until hit
            nx, ny = beam.d.nex_pos(x, y, n)
            if ny == y:
                seen[0].update((i, y) for i in range(x, nx, 1 if nx > x else -1))
            else:
                seen[1].update((x, i) for i in range(y, ny, 1 if ny > y else -1))
            x, y = nx, ny
        if (x, y) not in grid:
            continue
        (b1, b2) = grid[x, y].proj(beam.d)
        if b1:
            if (x, y) in seen[0]:
                continue
            seen[0].add((x, y))
        if b2:
            if (x, y) in seen[1]:
                continue
            seen[1].add((x, y))
        stack.extend(Beam(x, y, d) for d in grid[x, y].beam(beam.d))
    return seen[0].union(seen[1])


def scan(puzzle: Iterator[str]) -> Iterator[list[Type]]:
    for line in puzzle:
        if not (line := line.strip("\n")):
            continue
        yield [Type.from_str(c) for c in line]


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
