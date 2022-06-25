from typing import List


def print_(*values) -> int:
    print(*values, sep="", end="")

    return 0


def println_(*values) -> int:
    print(*values, sep="", end="\n")

    return 0


def input_() -> List[int]:
    return list(map(ord, input()))
