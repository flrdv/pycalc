from typing import List


def print_(*values) -> int:
    print(*values, sep="", end="")

    return 0


def println_(*values) -> int:
    print(*values, sep="", end="\n")

    return 0


def print_mem(mem: List) -> int:
    print(*mem, sep="", end="")

    return 0


def println_mem(mem: List) -> int:
    print(*mem, sep="", end="\n")

    return 0
