import bisect
import collections
import doctest
import operator
import re

day = "05"  # https://adventofcode.com/2023/day/5

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

Map = collections.namedtuple("Map", ["fr", "to", "dlt"])


def part_one(puzzle: list[str]) -> list[tuple[int, ...]]:
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

    >>> min(map(operator.itemgetter(-1), part_one(open(f"2023/day{day}.in"))))
    282277027
    """
    paths = []
    seeds, levels = scan(puzzle)
    for seed in seeds:
        path = [seed]
        for maps in levels:
            m = maps[bisect.bisect(maps, path[-1], key=operator.attrgetter("fr")) - 1]
            path.append(path[-1] + m.dlt if m.to > path[-1] else path[-1])
        paths.append(tuple(path))
    return paths


def part_two(puzzle: list[str]) -> list[tuple[int, int]]:
    """Solve part two of the puzzle.

    >>> part_two(example1.splitlines())
    [(46, 61), (82, 85), (86, 90), (94, 99)]

    >>> part_two(example1.splitlines())[0][0]
    46

    >>> part_two(open(f"2023/day{day}.in"))[0][0]
    11554135
    """
    seeds, levels = scan(puzzle)
    ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
    for maps in levels:
        new_ranges = []
        for r in ranges:
            while r[0] < r[1]:
                idx = bisect.bisect(maps, r[0], key=operator.attrgetter("fr")) - 1
                if (m := maps[idx]).to > r[0]:
                    dlt, to = m.dlt, m.to
                else:
                    dlt, to = 0, maps[idx + 1].fr if idx + 1 < len(maps) else r[1]
                new_ranges.append((r[0] + dlt, min(to, r[1]) + dlt))
                r = (to, r[1])
        ranges = []
        for r in sorted(new_ranges, key=operator.itemgetter(0)):
            if ranges and r[0] == ranges[-1][1]:
                ranges[-1] = (ranges[-1][0], r[1])
            else:
                ranges.append(r)
    return ranges


def scan(puzzle: list[str]) -> tuple[list[int], tuple[list[Map], ...]]:
    maps, seeds = [], []
    for line in puzzle:
        if line.startswith("seeds:"):
            seeds = list(map(int, re.findall(r"(\d+)+", line)))
        elif line.rstrip().endswith(":"):
            maps.append([(0, 0, 0)])  # bisect requires initial value
        elif line.rstrip():
            maps[-1].append(tuple(map(int, line.split())))
    for i in range(len(maps)):  # post-processing
        maps[i] = sorted(
            map(lambda t: Map(fr=t[1], to=t[1] + t[2], dlt=t[0] - t[1]), maps[i]),
            key=operator.itemgetter(0),
        )
    return seeds, tuple(maps)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
