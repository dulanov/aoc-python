import doctest
import functools
import itertools
from typing import Iterator

day = "12"  # https://adventofcode.com/2023/day/12

example1 = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


example2 = example1


def part_one(puzzle: list[str]) -> list[int]:
    """Solve part one of the puzzle.

    >>> part_one(example1.splitlines())
    [1, 4, 1, 1, 4, 10]

    >>> sum(part_one(example1.splitlines()))
    21

    >>> sum(part_one(open(f"2023/day{day}.in")))
    6958
    """
    return [arrange(pattern, *groups) for pattern, groups in scan(puzzle)]


def part_two(puzzle: list[str], copies: int = 5) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    [1, 16384, 1, 16, 2500, 506250]

    >>> sum(part_two(example2.splitlines()))
    525152

    >>> sum(part_two(open(f"2023/day{day}.in")))
    6555315065024
    """
    result = []
    for pattern, groups in scan(puzzle):
        pattern = "?".join(itertools.repeat(pattern, copies))
        result.append(arrange(pattern, *(groups * copies)))
    return result


@functools.cache
def arrange(pattern: str, *groups: int) -> int:
    """Found all possible arrangements of a pattern.

    >>> arrange("???.###", 1, 1, 3)
    1

    >>> arrange(".??..??...?##.", 1, 1, 3)
    4

    >>> arrange("?#?#?#?#?#?#?#?", 1, 3, 1, 6)
    1

    >>> arrange("????.#...#...", 4, 1, 1)
    1

    >>> arrange("????.######..#####.", 1, 6, 5)
    4

    >>> arrange("?###????????", 3, 2, 1)
    10
    """
    if not groups:
        return 0 if "#" in pattern else 1
    cnt, ln, pattern = 0, groups[0], pattern + "."
    if (min := sum(groups) + len(groups)) > len(pattern):
        return 0
    for offset in range(len(pattern) - min + 1):
        if is_group(pattern[offset : offset + ln + 1]):
            cnt += arrange(pattern[offset + ln + 1 :], *groups[1:])
        if pattern[offset] == "#":
            break
    return cnt


def is_group(pattern: str) -> bool:
    return "." not in pattern[:-1] and pattern[-1] != "#"


def scan(puzzle: list[str]) -> Iterator[tuple[str, list[int]]]:
    for line in puzzle:
        pattern, groups = line.split()
        yield pattern, list(map(int, groups.split(",")))


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
