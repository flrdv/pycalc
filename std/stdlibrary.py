from math import pi
from functools import reduce
from typing import Callable, Iterable

from . import stdmem, stdstatements, stdio


def _as_list(func: Callable) -> Callable[[Callable, Iterable], list]:
    def decorator(a: Callable, b: Iterable) -> list:
        return list(func(a, b))

    return decorator


stdnamespace = {
    "rt": lambda a, b: a ** (1/b),
    "sqrt": lambda a: a ** (1/2),
    "cbrt": lambda a: a ** (1/3),
    "pi": pi,

    "write": lambda target, value: target.write(value),
    "print": stdio.print_,
    "println": stdio.println_,
    "printmem": stdio.print_mem,
    "printlnmem": stdio.println_mem,
    "input": stdio.input_,
    "chr": chr,
    "ord": ord,

    "malloc": stdmem.mem_alloc,
    "mallocfor": stdmem.mem_allocfor,
    "get": stdmem.mem_get,
    "set": stdmem.mem_set,
    "sizeof": len,
    "call": lambda func: func(),

    "map": _as_list(map),
    "filter": _as_list(filter),
    "reduce": reduce,
    "while": stdstatements.while_,
    "if": stdstatements.if_else,
    "branch": stdstatements.branch,
}
