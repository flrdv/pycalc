from typing import List


def print_(*values) -> int:
    """
    Prints the given values to the console without a newline.

    Args:
        *values: The values to print.

    Returns:
        int: Always returns 0.
    """
    print(*values, sep="", end="")
    return 0


def println_(*values) -> int:
    """
    Prints the given values to the console with a newline.

    Args:
        *values: The values to print.

    Returns:
        int: Always returns 0.
    """
    print(*values, sep="", end="\n")
    return 0


def print_mem(mem: List) -> int:
    """
    Prints the contents of the given memory list to the console without a newline.

    Args:
        mem (List): The memory list to print.

    Returns:
        int: Always returns 0.
    """
    print(*mem, sep="", end="")
    return 0


def println_mem(mem: List) -> int:
    """
    Prints the contents of the given memory list to the console with a newline.

    Args:
        mem (List): The memory list to print.

    Returns:
        int: Always returns 0.
    """
    print(*mem, sep="", end="\n")
    return 0

