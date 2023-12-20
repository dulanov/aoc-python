from dataclasses import dataclass
import re
from typing import Iterator
import collections
import doctest

day = "19"

example1 = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


example2 = example1

Part = collections.namedtuple("Part", "x m a s")


@dataclass
class Rule:
    next: str
    category: int = 0
    left: int = 0
    right: int = 0

    def __call__(self, part: Part) -> tuple[bool, str]:
        if self.left and part[self.category] <= self.left:
            return False, ""
        if self.right and part[self.category] >= self.right:
            return False, ""
        return True, self.next


def part_one(puzzle: Iterator[str]) -> list[tuple[bool, list[int]]]:
    """Solve part one of the puzzle.

    >>> import pprint
    >>> pprint.pprint(part_one(example1.splitlines()))
    [(True, Part(x=787, m=2655, a=1222, s=2876)),
     (False, Part(x=1679, m=44, a=2067, s=496)),
     (True, Part(x=2036, m=264, a=79, s=2244)),
     (False, Part(x=2461, m=1339, a=466, s=291)),
     (True, Part(x=2127, m=1623, a=2188, s=1013))]

    >>> sum(map(lambda t: sum(t[1]) if t[0] else 0, part_one(example1.splitlines())))
    19114

    >>> sum(map(lambda t: sum(t[1]) if t[0] else 0, part_one(open(f"2023/day{day}.in"))))
    489392
    """
    (workflows, parts), res = scan(puzzle), []
    for part in parts:
        name = "in"
        while name not in ("A", "R"):
            name = process(workflows[name], part)
        res.append((name == "A", part))
    return res


def part_two(puzzle: Iterator[str]) -> list[int]:
    """Solve part two of the puzzle.

    >>> part_two(example2.splitlines())
    []

    >>> sum(part_two(example2.splitlines()))
    0

    >> sum(part_two(open(f"2023/day{day}.in")))
    ???
    """
    return []


def process(rules: list[Rule], part: Part) -> str:
    """Process a part through workflow and return the next.

    >>> p = Part(787, 2655, 1222, 2876)
    >>> process([Rule("px", 3, 0, 1351), Rule("qqz")], p)
    'qqz'

    >>> process([Rule("qs", 3, 2770, 0), Rule("hdj", 1, 0, 1801), Rule("R")], p)
    'qs'

    >>> process([Rule("A", 3, 3448, 0), Rule("lnx")], p)
    'lnx'

    >>> process([Rule("A", 1, 1548, 0), Rule("A")], p)
    'A'
    """
    for rule in rules:
        done, next = rule(part)
        if done:
            return next
    raise ValueError(f"Could not process {part}")


def scan(puzzle: Iterator[str]) -> tuple[dict[str, list[Rule]], list[Part]]:
    workflows, parts = {}, []
    wr = re.compile(r"(?P<n>\w+){(.+),(?P<l>\w+)}")
    rr = re.compile(r"(?P<c>\w+)([<>])(?P<d>\d+):(?P<n>\w+)")
    pr = re.compile(r"{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}")
    for line in puzzle:
        if not line.strip("\n"):
            continue
        if not line.startswith("{"):
            m, rules = wr.match(line.strip("\n")), []
            for m2 in rr.finditer(m.group(2)):
                left = int(m2["d"]) if m2.group(2) == ">" else 0
                right = int(m2["d"]) if m2.group(2) == "<" else 0
                rules.append(Rule(m2["n"], "xmas".index(m2["c"]), left, right))
            rules.append(Rule(m["l"]))
            workflows[m["n"]] = rules
            continue
        m = pr.match(line.strip("\n"))
        parts.append(Part(int(m["x"]), int(m["m"]), int(m["a"]), int(m["s"])))
    return workflows, parts


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
