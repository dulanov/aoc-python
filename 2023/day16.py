from __future__ import annotations
from collections import deque, namedtuple
from enum import Enum
from typing import Iterator
import doctest
import operator

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


class Dir(Enum):
    U, D, L, R = range(4)

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

    def projection(self, d: Dir) -> tuple[bool, bool]:
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
    return diagram(solve(grid, Beam(-1, 0, Dir.R)))


def part_two(puzzle: Iterator[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    (51, Beam(x=3, y=-1, d=<Dir.D: 1>))

    >>> part_two(example2.splitlines())[0]
    51

    >>> part_two(open(f"2023/day{day}.in"))[0]
    8331
    """
    grid, rs = [tiles for tiles in scan(puzzle)], (0, None)
    for (x, y), (dx, dy), d in [
        ((0, -1), (1, 0), Dir.D),
        ((-1, 0), (0, 1), Dir.R),
        ((0, len(grid)), (1, 0), Dir.U),
        ((len(grid), 0), (0, 1), Dir.L),
    ]:
        for i in range(len(grid)):
            beam = Beam(x + i * dx, y + i * dy, d)
            if (v := energized_tiles(solve(grid, beam))) > rs[0]:
                rs = (v, beam)
    return rs


def solve(grid: list[list[tuple[Type, int]]], beam: Beam) -> list[list[bool]]:
    stack, visited = deque([beam]), (
        [[False] * len(grid[0]) for _ in range(len(grid))],
        [[False] * len(grid[0]) for _ in range(len(grid))],
    )
    while stack:
        beam = stack.pop()
        x, y = beam.d.nex_pos(beam.x, beam.y)
        if not (0 <= x < len(grid[0]) and 0 <= y < len(grid)):
            continue
        tile, (b1, b2) = grid[y][x], grid[y][x].projection(beam.d)
        if visited[0][y][x] and b1 or visited[1][y][x] and b2:
            continue
        visited[0][y][x], visited[1][y][x] = b1, b2
        stack.extend(Beam(x, y, d) for d in tile.beam(beam.d))
    return [
        list(map(operator.or_, tiles1, tiles2))
        for tiles1, tiles2 in zip(visited[0], visited[1])
    ]


def diagram(visited: list[list[bool]]) -> str:
    result = []
    for tiles in visited:
        result.append("".join(map(lambda t: "#" if t else ".", tiles)))
    return "\n".join(result)


def energized_tiles(visited: list[list[bool]]) -> int:
    return sum(sum(t for t in tiles) for tiles in visited)


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
