from pycalc.tokentypes.types import ArgumentsError


def print_(*floats) -> int:
    if any(not num.is_integer() for num in floats):
        raise ArgumentsError("print() takes only integers")

    print(*[chr(int(num)) for num in floats], sep="", end="")

    return 0
