from typing import TypeVar, Sequence

T = TypeVar("T")


def concat(*s: Sequence[T] | T) -> Sequence[T]:
    elems = []
    for x in s:
        if x is None:
            continue
        elems.extend(x) if isinstance(x, list) else elems.append(x)
    return elems
