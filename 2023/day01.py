from typing import Iterable, Iterator
import doctest

day = "01"

example1 = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

example2 = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

replacements = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "4",
    "five": "5e",
    "six": "6",
    "seven": "7n",
    "eight": "e8t",
    "nine": "n9e",
}


def part_one(puzzle: Iterable[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    [12, 38, 15, 77]

    >>> sum(part_one(example1.splitlines()))
    142

    >>> sum(part_one(open(f"2023/day{day}.in").readlines()))
    55130
    """
    return [t[0] * 10 + t[-1] for t in scan(puzzle)]


def part_two(puzzle: Iterable[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    [29, 83, 13, 24, 42, 14, 76]

    >>> sum(part_two(example2.splitlines()))
    281

    >>> sum(part_two(open(f"2023/day{day}.in").readlines()))
    54985
    """
    return [t[0] * 10 + t[-1] for t in scan(puzzle, replacements)]


def scan(puzzle: Iterable[str], reps: dict[str, str] = {}) -> Iterator[tuple[int, ...]]:
    for line in puzzle:
        for k, v in reps.items():
            line = line.replace(k, v)
        digits = [c for c in line if c.isdigit()]
        yield tuple(map(int, digits))


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
