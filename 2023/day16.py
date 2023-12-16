from __future__ import annotations
import collections
import copy
from enum import Enum
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


Beam = collections.namedtuple("Beam", ["x", "y", "d"])


class Dir(Enum):
    U, D, L, R = range(4)

    def nex_pos(self, x: int, y: int) -> tuple[int, int]:
        return (
            x + (self == Dir.R) - (self == Dir.L),
            y + (self == Dir.D) - (self == Dir.U),
        )


class Tile:
    """A tile of the contraption."""

    def __init__(self, c: str) -> None:
        self.value = c
        self.__visited = [False] * len(Dir.__members__)

    def __repr__(self) -> str:
        return self.value

    def energized(self) -> bool:
        return any(self.__visited)

    def visited(self, d: Dir) -> bool:
        return self.__visited[d.value]

    def visit(self, d: Dir) -> list[Dir]:
        self.__visited[d.value] = True

    @classmethod
    def from_str(cls, c: str) -> Tile:
        return {
            ".": EmptyTile,
            "/": MirrorTile,
            "\\": MirrorBackslashTile,
            "-": SplitterHorizontalTile,
            "|": SplitterVerticalTile,
        }[c]()


class EmptyTile(Tile):
    def __init__(self) -> None:
        super().__init__(".")

    def process_beam(self, d: Dir) -> list[Dir]:
        self.visit(d)
        return [d]


class MirrorTile(Tile):
    def __init__(self) -> None:
        super().__init__("/")

    def process_beam(self, d: Dir) -> list[Dir]:
        self.visit(d)
        return ([Dir.R], [Dir.L], [Dir.D], [Dir.U])[d.value]


class MirrorBackslashTile(Tile):
    def __init__(self) -> None:
        super().__init__("\\")

    def process_beam(self, d: Dir) -> list[Dir]:
        self.visit(d)
        return ([Dir.L], [Dir.R], [Dir.U], [Dir.D])[d.value]


class SplitterHorizontalTile(Tile):
    def __init__(self) -> None:
        super().__init__("-")

    def process_beam(self, d: Dir) -> list[Dir]:
        self.visit(d)
        return ([Dir.L, Dir.R], [Dir.L, Dir.R], [Dir.L], [Dir.R])[d.value]


class SplitterVerticalTile(Tile):
    def __init__(self) -> None:
        super().__init__("|")

    def process_beam(self, d: Dir) -> list[Dir]:
        self.visit(d)
        return ([Dir.U], [Dir.D], [Dir.U, Dir.D], [Dir.U, Dir.D])[d.value]


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
    grid, res = [tiles for tiles in scan(puzzle)], (0, None)
    for (x, y), d, (dx, dy) in [
        ((0, -1), Dir.D, (1, 0)),
        ((-1, 0), Dir.R, (0, 1)),
        ((0, len(grid)), Dir.U, (1, 0)),
        ((len(grid), 0), Dir.L, (0, 1)),
    ]:
        for i in range(len(grid)):
            beam = Beam(x + i * dx, y + i * dy, d)
            if (v := energized_tiles(solve(grid, beam))) > res[0]:
                res = (v, beam)
    return res


def solve(grid: list[list[Tile]], beam: Beam) -> list[list[Tile]]:
    grid, stack = copy.deepcopy(grid), [beam]
    while stack:
        beam = stack.pop()
        x, y = beam.d.nex_pos(beam.x, beam.y)
        if not (0 <= x < len(grid[0]) and 0 <= y < len(grid)):
            continue
        if (tile := grid[y][x]).visited(beam.d):
            continue
        stack += [Beam(x, y, d) for d in tile.process_beam(beam.d)]
    return grid


def diagram(grid: list[list[Tile]]) -> str:
    result = []
    for tiles in grid:
        result.append("".join(map(lambda t: "#" if t.energized() else ".", tiles)))
    return "\n".join(result)


def energized_tiles(grid: list[list[Tile]]) -> int:
    return sum(sum(t.energized() for t in tiles) for tiles in grid)


def scan(puzzle: Iterator[str]) -> Iterator[list[Tile]]:
    for line in puzzle:
        if not (line := line.strip("\n")):
            continue
        yield [Tile.from_str(c) for c in line]


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
