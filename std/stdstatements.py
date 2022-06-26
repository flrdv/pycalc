from itertools import islice
from typing import Callable, Optional, Union

from pycalc.tokentypes.types import Number, ArgumentsError


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


def branch(*values: Union[Number, Callable]) -> int:
    """
    This is also kind of if, but a bit better
    """

    if len(values) < 2 or callable(values[0]):
        raise ArgumentsError("invalid arguments")

    pairs = zip(
        islice(values, None, None, 2),
        islice(values, 1, None, 2)
    )

    for cond, callback in pairs:
        if cond:
            return callback()

    if len(values) % 2:
        return values[-1]()

    return 0
