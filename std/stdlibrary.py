from math import pi, sqrt
from functools import reduce

from . import stdmem, stdstatements, stdio


stdnamespace = {
    "rt": lambda a, b: a ** (1/b),
    "sqrt": lambda a: a ** (1/2),
    "cbrt": lambda a: a ** (1/3),
    "pi": pi,

    "write": lambda target, value: target.write(value),
    "print": stdio.print_,
    "println": stdio.println_,

    "malloc": stdmem.mem_alloc,
    "get": stdmem.mem_get,
    "set": stdmem.mem_set,
    "sizeof": len,
    "call": lambda func: func(),

    "map": map,
    "filter": filter,
    "reduce": reduce,
    "cond": stdstatements.cond,
    "if": stdstatements.if_,
}
