from __future__ import annotations
from enum import Enum
from typing import Iterator
import doctest
import heapq

day = "17"

example1 = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""


example21 = example1

example22 = """\
111111111111
999999999991
999999999991
999999999991
999999999991
"""


class Dir(Enum):
    U, R, D, L = range(4)

    def __lt__(self, other: Dir) -> bool:
        return self.value < other.value

    def clockwise(self) -> Dir:
        return Dir((self.value + 1) % 4)

    def counter_clockwise(self) -> Dir:
        return Dir((self.value - 1) % 4)

    def next_pos(self, x: int, y: int, n: int = 1) -> tuple[int, int]:
        return (
            x + n * ((self == Dir.R) - (self == Dir.L)),
            y + n * ((self == Dir.D) - (self == Dir.U)),
        )


def part_one(puzzle: Iterator[str]) -> int:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    102

    >>> part_one(open(f"2023/day{day}.in"))
    1076
    """
    return solve(list(scan(puzzle)))


def part_two(puzzle: Iterator[str]) -> int:
    """Solve part two of the puzzle.

    >>> part_two(example21.splitlines())
    94

    >>> part_two(example22.splitlines())
    71

    >>> part_two(open(f"2023/day{day}.in"))
    1219
    """
    return solve(list(scan(puzzle)), min=4, max=10)


def solve(grid: list[list[int]], /, *, min: int = 1, max: int = 3) -> int:
    pq, seen = [(0, 0, 0, Dir.R), (0, 0, 0, Dir.D)], set()
    while pq:
        n, x, y, d = heapq.heappop(pq)
        if x == len(grid[0]) - 1 and y == len(grid) - 1:
            return n
        if (x, y, d) in seen:
            continue
        seen.add((x, y, d))
        for d in [d.counter_clockwise(), d.clockwise()]:
            costs = []
            for i in range(1, max + 1):
                nx, ny = d.next_pos(x, y, i)
                if nx < 0 or ny < 0 or nx >= len(grid[0]) or ny >= len(grid):
                    break
                costs.append(grid[ny][nx])
                if i >= min:
                    heapq.heappush(pq, (n + sum(costs), nx, ny, d))


def scan(puzzle: Iterator[str]) -> Iterator[list[int]]:
    for line in puzzle:
        yield [int(c) for c in line.strip("\n")]


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
