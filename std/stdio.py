def print_(*numbers) -> int:
    print(*[chr(int(num)) for num in numbers], sep="", end="")

    return 0


def println_(*numbers) -> int:
    print(*[chr(int(num)) for num in numbers], sep="", end="\n")

    return 0
