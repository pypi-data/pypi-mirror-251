from typing import TypeVar

T = TypeVar('T')


def zero(v: T) -> T:
    return type(v)()
