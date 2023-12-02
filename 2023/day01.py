from typing import Iterable, Iterator
import doctest
import re

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
    "one": "1ne",
    "two": "2wo",
    "three": "3hree",
    "four": "4our",
    "five": "5ive",
    "six": "6ix",
    "seven": "7even",
    "eight": "8ight",
    "nine": "9ine",
}


def part_one(puzzle: Iterable[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    [12, 38, 15, 77]

    >>> sum(part_one(example1.splitlines()))
    142

    >>> sum(part_one(read(f"2023/day{day}.in")))
    55130
    """
    return [t[0] * 10 + t[-1] for t in scan(puzzle)]


def part_two(puzzle: Iterable[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    [29, 83, 13, 24, 42, 14, 76]

    >>> sum(part_two(example2.splitlines()))
    281

    >>> sum(part_two(read(f"2023/day{day}.in")))
    54985
    """
    return [t[0] * 10 + t[-1] for t in scan(puzzle, replacements)]


def scan(puzzle: Iterable[str], reps: dict[str, str] = []) -> Iterator[tuple[int, ...]]:
    for line in puzzle:
        if reps:
            if m := re.search(rf"{'|'.join(reps.keys())}", line):
                line = line.replace(m.group(), reps[m.group()], 1)
            if m := re.search(rf"{'|'.join(map(rev, reps.keys()))}", rev(line)):
                line = rev(rev(line).replace(m.group(), rev(reps[rev(m.group())]), 1))
        digits = [c for c in line if c.isdigit()]
        yield tuple(map(int, digits))


def rev(s: str) -> str:
    return s[::-1]


def read(file: str) -> Iterator[str]:
    with open(file, "r") as file:
        for line in file:
            yield line


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
