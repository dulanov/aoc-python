from typing import Iterable, Iterator
import doctest
import functools
import operator

day = "12"

example1 = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


example2 = example1


def part_one(puzzle: Iterable[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    [1, 4, 1, 1, 4, 10]

    >>> sum(part_one(example1.splitlines()))
    21

    >>> sum(part_one(open(f"2023/day{day}.in").readlines()))
    6958
    """
    result = []
    for pattern, groups in scan(puzzle):
        result.append(len(arrange(pattern, *groups)))
    return result


def part_two(puzzle: Iterable[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    []

    >>> sum(part_two(example2.splitlines()))
    0

    >> sum(part_two(open(f"2023/day{day}.in").readlines()))
    ???
    """
    return []


def arrange(pattern: str, *groups: list[int]) -> list[str]:
    """Found all possible arrangements of a pattern.

    >>> import pprint
    >>> pprint.pprint(arrange("???.###", 1, 1, 3))
    ['#.#.###']

    >>> pprint.pprint(arrange(".??..??...?##.", 1, 1, 3))
    ['.#...#....###.', '.#....#...###.', '..#..#....###.', '..#...#...###.']

    >>> pprint.pprint(arrange("?#?#?#?#?#?#?#?", 1, 3, 1, 6))
    ['.#.###.#.######']

    >>> pprint.pprint(arrange("????.#...#...", 4, 1, 1))
    ['####.#...#...']

    >>> pprint.pprint(arrange("????.######..#####.", 1, 6, 5))
    ['#....######..#####.',
     '.#...######..#####.',
     '..#..######..#####.',
     '...#.######..#####.']

    >>> pprint.pprint(arrange("?###????????", 3, 2, 1))
    ['.###.##.#...',
     '.###.##..#..',
     '.###.##...#.',
     '.###.##....#',
     '.###..##.#..',
     '.###..##..#.',
     '.###..##...#',
     '.###...##.#.',
     '.###...##..#',
     '.###....##.#']
    """
    stack = ([], [(pattern + ".", 0)])
    for i, n in enumerate(groups):
        stack = stack[1], []
        ln = sum(groups[i:]) + len(groups[i:])
        for rec, pos in stack[0]:
            if len(rec) - pos < ln:
                continue
            for j in range(pos, len(rec) - ln + 1):
                if is_group(rec[j : j + n + 1]):
                    fst, grp, lst = rec[:pos], group(n, j - pos), rec[j + n + 1 :]
                    if i == len(groups) - 1:
                        if "#" in lst:
                            if rec[j] == "#":
                                break
                            continue
                        lst = lst.replace("?", ".")
                    stack[1].append((fst + grp + lst, j + n + 1))
                if rec[j] == "#":
                    break
    return list(map(lambda t: t[0][:-1], stack[1]))


def group(n, m: int) -> str:
    return "." * m + "#" * n + "."


def is_group(pattern: str) -> bool:
    return "." not in pattern[:-1] and pattern[-1] != "#"


def scan(puzzle: Iterable[str]) -> Iterator[tuple[str, list[int]]]:
    for line in puzzle:
        pattern, groups = line.split()
        yield pattern, list(map(int, groups.split(",")))


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
