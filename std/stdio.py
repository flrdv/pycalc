from typing import List


def print_(*numbers) -> int:
    print(*[chr(int(num)) for num in numbers], sep="", end="")

    return 0


def println_(*numbers) -> int:
    print(*[chr(int(num)) for num in numbers], sep="", end="\n")

    return 0


def input_() -> List[int]:
    return list(map(ord, input()))
