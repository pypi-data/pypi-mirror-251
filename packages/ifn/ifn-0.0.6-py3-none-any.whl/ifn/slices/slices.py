from typing import TypeVar, Sequence

T = TypeVar("T")


def concat(*s: Sequence[T] | T) -> Sequence[T]:
    elems = []
    for x in s:
        if x is None:
            continue
        elems.extend(x) if isinstance(x, list) else elems.append(x)
    return elems


def insert[T](s: Sequence[T], elem: T | Sequence[T], i: int = None) -> Sequence[T]:
    i = len(s) if i is None else i
    s[i:i + 1] = elem if isinstance(elem, list) else [elem]
    return s
