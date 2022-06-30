from typing import List


def mem_alloc(size: int) -> List[int]:
    return [0] * size


def mem_allocfor(*values: int) -> List[int]:
    return list(values)


def mem_get(mem: List[int], offset: int) -> int:
    if 0 > offset >= len(mem):
        return -1

    return mem[offset]


def mem_set(mem: List[int], offset: int, value: int) -> int:
    if 0 > offset or offset >= len(mem) or 0 > value > 255:
        return -1

    mem[offset] = value
    return 0


def slice_(mem: List[int], begin: int, end: int) -> List[int]:
    return mem[begin:end]
