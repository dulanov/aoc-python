import functools
from typing import Iterable, Iterator
import doctest
import re

day = "02"

example1 = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

example2 = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


class RGB:
    """RGB color representation of sets of cubes."""

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return f"RGB({self.r}, {self.g}, {self.b})"

    @classmethod
    def union(cls, l, r):
        return RGB(max(l.r, r.r), max(l.g, r.g), max(l.b, r.b))


def part_one(
    puzzle: Iterable[str], limits: RGB = RGB(12, 13, 14)
) -> list[tuple[int, bool]]:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    [1, 2, 5]

    >>> sum(part_one(example1.splitlines()))
    8

    >>> sum(part_one(read(f"2023/day{day}.in")))
    2101
    """
    i, result = 0, []
    for game in scan(puzzle):
        i, game = i + 1, functools.reduce(lambda x, y: RGB.union(x, y), game)
        if game.r <= limits.r and game.g <= limits.g and game.b <= limits.b:
            result.append(i)
    return result


def part_two(puzzle: Iterable[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    [48, 12, 1560, 630, 36]

    >>> sum(part_two(example2.splitlines()))
    2286

    >>> sum(part_two(read(f"2023/day{day}.in")))
    58269
    """
    result = []
    for game in scan(puzzle):
        game = functools.reduce(lambda x, y: RGB.union(x, y), game)
        result.append(game.r * game.g * game.b)
    return result


def scan(puzzle: Iterable[str]) -> Iterator[list[RGB]]:
    r1 = re.compile(r"Game (?:\d+): (?P<sets>.*)")
    r2 = re.compile(r"(?P<cubes>\d+) (?P<color>\w+)")
    games = []
    for line in puzzle:
        game = []
        for s in (r1.search(line).group("sets")).split("; "):
            r, g, b = 0, 0, 0
            for c in r2.finditer(s):
                if c.group("color") == "red":
                    r = int(c.group("cubes"))
                elif c.group("color") == "green":
                    g = int(c.group("cubes"))
                elif c.group("color") == "blue":
                    b = int(c.group("cubes"))
            game.append(RGB(r, g, b))
        games.append(game)
    return games


def read(file: str) -> Iterator[str]:
    with open(file, "r") as file:
        for line in file:
            yield line


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
