from typing import Iterable
import doctest
import itertools
import re

day = "08"

example1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

example2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


def part_one(puzzle: Iterable[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    ['AAA', 'CCC', 'ZZZ']

    >>> len(part_one(example1.splitlines())) - 1
    2

    >>> part_one(example2.splitlines())
    ['AAA', 'BBB', 'AAA', 'BBB', 'AAA', 'BBB', 'ZZZ']

    >>> len(part_one(example2.splitlines())) - 1
    6

    >>> len(part_one(open(f"2023/day{day}.in").readlines())) - 1
    12083
    """
    ins, nodes = scan(puzzle)
    nodes, path = {n[0]: n[1:] for n in nodes}, ["AAA"]
    for i in itertools.cycle(ins):
        if path[-1] == "ZZZ":
            break
        path.append(nodes[path[-1]][i])
    return path


def part_two(puzzle: Iterable[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example1.splitlines())
    []

    >>> sum(part_two(example2.splitlines()))
    0

    >> sum(part_two(open(f"2023/day{day}.in").readlines()))
    ???
    """
    return []


def scan(puzzle: Iterable[str]) -> tuple[list[int], list[tuple[str, str, str]]]:
    ins, nodes, r = [], [], re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")
    for line in puzzle:
        if not ins:
            ins = [1 if c == "R" else 0 for c in line.strip()]
        elif line.strip():
            nodes.append(r.match(line).groups())
    return ins, nodes


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
