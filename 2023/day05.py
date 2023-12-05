import bisect
import operator
from typing import Iterable, Iterator
import collections
import doctest
import re

day = "05"

example1 = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

example2 = example1

Range = collections.namedtuple("Range", ["frm", "num", "dlt"])


def part_one(puzzle: Iterable[str]) -> list[tuple[int, ...]]:
    """Solve part one of the puzzle.

    >>> import pprint
    >>> pprint.pprint(part_one(example1.splitlines()))
    [(79, 81, 81, 81, 74, 78, 78, 82),
     (14, 14, 53, 49, 42, 42, 43, 43),
     (55, 57, 57, 53, 46, 82, 82, 86),
     (13, 13, 52, 41, 34, 34, 35, 35)]

    >>> import operator
    >>> min(map(operator.itemgetter(-1), part_one(example1.splitlines())))
    35

    >>> min(map(operator.itemgetter(-1), part_one(open(f"2023/day{day}.in").readlines())))
    282277027
    """
    paths = []
    seeds, maps = scan(puzzle)
    for seed in seeds:
        path = [seed]
        for m in maps:
            i = bisect.bisect(m, path[-1], key=operator.attrgetter("frm"))
            r = m[i - 1] if i else Range(0, 0, 0)
            path.append(path[-1] + r.dlt if r.frm + r.num >= path[-1] else path[-1])
        paths.append(tuple(path))
    return paths


def part_two(puzzle: Iterable[str], n: int) -> list[int]:
    """Solve part two of the puzzle."""
    return []


def scan(puzzle: Iterable[str]) -> tuple[list[int], tuple[list[Range], ...]]:
    maps = []
    for line in puzzle:
        if line.startswith("seeds:"):
            seeds = list(map(int, re.findall(r"(\d+)+", line)))
        elif line.rstrip().endswith("map:"):
            maps.append([])
        elif line.rstrip():
            maps[-1].append(tuple(map(int, line.split())))
    for i in range(len(maps)):
        maps[i] = sorted(
            map(lambda t: Range(t[1], t[2], t[0] - t[1]), maps[i]),
            key=operator.itemgetter(0),
        )
    return seeds, tuple(maps)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
