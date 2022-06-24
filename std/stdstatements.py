from typing import Callable

from pycalc.tokentypes.types import Number


def cond(condition: Callable, if_cb: Callable, else_cb: Callable) -> Number:
    return if_cb() if condition() else else_cb()


def if_(condition: Callable, cb: Callable) -> int:
    if condition():
        cb()

    return 0
