from typing import Iterable, Iterator
import doctest

day = "13"

example1 = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


example2 = example1


def part_one(puzzle: Iterable[str]) -> list[int]:
    """Solve part one of the puzzle.

    >> part_one(example1.splitlines())
    [(5, 0), (0, 4)]

    >> sum(map(lambda t: t[0] + t[1] * 100, part_one(example1.splitlines())))
    405

    >>> sum(map(lambda t: t[0] + t[1] * 100, part_one(open(f"2023/day{day}.in"))))
    33356
    """
    result = []
    for pattern in scan(puzzle):
        cols = fold(transpose(pattern))
        for i in range(1, len(cols)):
            if reflected(cols, i):
                result.append((i, 0))
                break
        else:
            rows = fold(pattern)
            for i in range(1, len(rows)):
                if reflected(rows, i):
                    result.append((0, i))
                    break
    return result


def part_two(puzzle: Iterable[str], copies: int = 5) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    [(0, 3), (0, 1)]

    >>> sum(map(lambda t: t[0] + t[1] * 100, part_two(example2.splitlines())))
    400

    >> sum(map(lambda t: t[0] + t[1] * 100, part_two(open(f"2023/day{day}.in"))))
    28475
    """
    result = []
    for pattern in scan(puzzle):
        cols = fold(transpose(pattern))
        for i in range(1, len(cols)):
            if reflected(cols, i, bits=1):
                result.append((i, 0))
        rows = fold(pattern)
        for i in range(1, len(rows)):
            if reflected(rows, i, bits=1):
                result.append((0, i))
    return result


def reflected(ns: list[int], pos: int, bits: int = 0) -> bool:
    for i in range(min(pos, len(ns) - pos)):
        if d := ns[pos - i - 1] ^ ns[pos + i]:
            bits -= d.bit_count()
    return bits == 0


def transpose(pattern: list[list[bool]]) -> list[list[bool]]:
    return list(map(list, zip(*pattern)))


def fold(pattern: list[list[bool]]) -> list[int]:
    return [as_num(row) for row in pattern]


def as_num(pattern: list[bool]) -> int:
    return sum(2**i for i, b in enumerate(pattern) if b)


def scan(puzzle: Iterable[str]) -> Iterator[list[list[bool]]]:
    pattern = []
    for line in puzzle:
        if line.strip():
            pattern.append([c == "#" for c in line.strip()])
            continue
        yield pattern
        pattern = []
    yield pattern


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
