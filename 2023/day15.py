from typing import Iterator
import doctest

day = "15"

example1 = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


example2 = example1


def part_one(puzzle: Iterator[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    [30, 253, 97, 47, 14, 180, 9, 197, 48, 214, 231]

    >>> sum(part_one(example1.splitlines()))
    1320

    >>> sum(part_one(open(f"2023/day{day}.in")))
    506891
    """
    return [calc_hash(line) for line in scan(puzzle)]


def part_two(puzzle: Iterator[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    []

    >>> len(part_two(example2.splitlines()))
    0

    >> len(part_two(open(f"2023/day{day}.in")))
    ???
    """
    return []


def calc_hash(s: str) -> int:
    """Holiday ASCII String Helper algorithm (appendix 1A).

    >>> calc_hash("HASH")
    52
    """
    hash = 0
    for c in s:
        hash = ((hash + ord(c)) * 17) % 256
    return hash


def scan(puzzle: Iterator[str]) -> list[str]:
    for line in puzzle:
        return line.strip().split(",")


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
