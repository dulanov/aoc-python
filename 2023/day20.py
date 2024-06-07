import collections
import doctest
import itertools
import operator
import typing
from abc import abstractmethod
from itertools import chain
from typing import Callable, Iterable, Iterator, cast

day = "20"  # https://adventofcode.com/2023/day/20

example11 = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

example12 = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""

example2 = example12

Pulse = typing.NamedTuple("Pulse", [("tx", str), ("rx", str), ("hp", bool)])


class Module:
    def __init__(self, dest: Iterable[str]) -> None:
        self._dest = list(dest)

    @abstractmethod
    def receive(self, tx: str, hp: bool) -> Iterator[tuple[str, bool]]:
        pass


class Broadcaster(Module):
    def receive(self, tx: str, hp: bool) -> Iterator[tuple[str, bool]]:
        return ((rx, hp) for rx in self._dest)


class FlipFlop(Module):
    def __init__(self, dest: Iterable[str]) -> None:
        super().__init__(dest)
        self._state = False

    def receive(self, tx: str, hp: bool) -> Iterator[tuple[str, bool]]:
        if hp:
            return iter(())
        self._state = not self._state
        return ((rx, self._state) for rx in self._dest)


class Inverter(Module):
    def __init__(self, dest: Iterable[str]) -> None:
        super().__init__(dest)
        self._state = collections.defaultdict(bool)
        self._inputs = 0

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, value):
        self._inputs = value

    def receive(self, tx: str, hp: bool) -> Iterator[tuple[str, bool]]:
        self._state[tx] = hp
        v = sum(self._state.values()) != self._inputs
        return ((rx, v) for rx in self._dest)


def part_one(puzzle: list[str], n: int = 1_000) -> tuple[int, int]:
    """Solve part one of the puzzle.

    >>> part_one(example11.splitlines())
    (8000, 4000)

    >>> import math
    >>> math.prod(part_one(example11.splitlines()))
    32000000

    >>> part_one(example12.splitlines())
    (4250, 2750)

    >>> math.prod(part_one(example12.splitlines()))
    11687500

    >>> math.prod(part_one(open(f"2023/day{day}.in")))
    680278040
    """
    modules, rs = dict(scan(puzzle)), [0, 0]
    for d in chain.from_iterable(m._dest for m in modules.values()):
        if d in modules and isinstance(modules[d], Inverter):
            cast(Inverter, modules[d]).inputs += 1
    for _ in range(n):
        cycle(modules, lambda _, hp: operator.setitem(rs, hp, rs[hp] + 1))
    return cast(tuple[int, int], tuple(rs))


def part_two(puzzle: list[str]) -> tuple[int, int, int, int]:
    """Solve part two of the puzzle.

    >>> import math
    >>> math.lcm(*part_two(open(f"2023/day{day}.in")))
    243548140870057
    """
    modules, rs = dict(scan(puzzle)), []
    for d in chain.from_iterable(m._dest for m in modules.values()):
        if d in modules and isinstance(modules[d], Inverter):
            cast(Inverter, modules[d]).inputs += 1
    for i in itertools.count(1):
        if len(rs) == 4:
            break
        # 'vf' is just invertor before `rx`
        cycle(modules, lambda rx, hp: rs.append(i) if rx == "vf" and hp else None)
    return tuple(rs)


def cycle(modules: dict[str, Module], fn: Callable[[str, bool], None]) -> None:
    q = collections.deque([Pulse("button", "broadcaster", False)])
    while q:
        tx, rx, hq = q.popleft()
        fn(rx, hq)
        if rx not in modules:
            continue
        for rx2, hp2 in modules[rx].receive(tx, hq):
            q.append(Pulse(rx, rx2, hp2))


def scan(puzzle: list[str]) -> Iterator[tuple[str, Module]]:
    for line in puzzle:
        src, dest = line.strip("\n").split(" -> ")
        if src.startswith("%"):
            yield src[1:], FlipFlop(dest.split(", "))
        elif src.startswith("&"):
            yield src[1:], Inverter(dest.split(", "))
        else:
            yield src, Broadcaster(dest.split(", "))


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == "__main__":
    doctest.testmod()
