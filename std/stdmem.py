from typing import List

from pycalc.tokentypes.types import Number


def mem_alloc(size: Number) -> List[int]:
    if not size.is_integer():
        raise TypeError("malloc() takes only integers")

    return [0] * int(size)


def mem_get(mem: List[int], offset: Number) -> int:
    if not offset.is_integer():
        raise TypeError("get() takes only integers")

    if 0 > offset >= len(mem):
        return -1

    return mem[int(offset)]


def mem_set(mem: List[int], offset: Number, value: Number) -> int:
    if not offset.is_integer() or not value.is_integer():
        raise TypeError("set() takes only integers")

    if 0 > offset >= len(mem) or 0 > value > 255:
        return -1

    mem[int(offset)] = value
    return 0
