from typing import TypeVar

T = TypeVar("T")


def append(s: T = None, *elem: T | object) -> T:
    elems = []
    for x in elem:
        elems.extend(x) if isinstance(x, list) else elems.append(x)
    return [*s, *elems] if s else elems
