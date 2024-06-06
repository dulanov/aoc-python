import doctest
from typing import Iterator

day = "21"

example1 = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


example2 = example1


def part_one(puzzle: Iterator[str], n: int = 64) -> list[int]:
    """Solve part one of the puzzle.

    >> import pprint
    >> pprint.pprint(part_one(example1.splitlines(), n=6))
    [(2, 8),
     (3, 1),
     (3, 3),
     (3, 5),
     (3, 7),
     (4, 0),
     (4, 2),
     (4, 8),
     (5, 3),
     (5, 5),
     (6, 4),
     (6, 6),
     (7, 1),
     (7, 3),
     (7, 5),
     (9, 3)]

    >> sum(part_one(example1.splitlines()))
    16

    >> sum(part_one(open(f"2023/day{day}.in")))
    ???
    """
    return []


def part_two(puzzle: Iterator[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    []

    >>> sum(part_two(example2.splitlines()))
    0

    >> sum(part_two(open(f"2023/day{day}.in")))
    ???
    """
    return []


def scan(puzzle: Iterator[str]) -> Iterator[str]:
    for line in puzzle:
        yield line.strip("\n")


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
