from math import pi, sqrt
from functools import reduce

from . import stdmem, stdstatements, stdio


stdnamespace = {
    "sqrt": sqrt,
    "cbrt": lambda a, b: a ** (b/3),
    "pi": pi,

    "write": lambda target, value: target.write(value),
    "print": stdio.print_,

    "malloc": stdmem.mem_alloc,
    "get": stdmem.mem_get,
    "set": stdmem.mem_set,

    "map": map,
    "filter": filter,
    "reduce": reduce,
    "cond": stdstatements.cond,
    "if": stdstatements.if_,
}
