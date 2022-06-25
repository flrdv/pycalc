from typing import Callable, Optional

from pycalc.tokentypes.types import Number


def if_else(
        condition: Number,
        if_cb: Callable,
        else_cb: Optional[Callable] = None) -> Number:
    if else_cb is None:
        return _if(condition, if_cb)

    return if_cb() if condition else else_cb()


def _if(condition: Number, cb: Callable) -> int:
    return cb() if condition else 0


def while_(condition: Callable, body: Callable) -> int:
    while condition():
        body()

    return 0
