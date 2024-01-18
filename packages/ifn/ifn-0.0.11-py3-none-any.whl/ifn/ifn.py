from typing import TypeVar, Sequence, Callable

T = TypeVar('T')


def zero(v: T) -> T:
    return type(v)()


def for_each(s: Sequence, f: Callable[[...], None]):
    s = s.items() if isinstance(s, dict) else s
    if isinstance(s, dict):
        for x in s.items(): f(*x)
        return
    for x in s:
        x = next(iter(x.items())) if isinstance(x, dict) else x
        f(*x)
