from typing import TypeVar

S = TypeVar("S", bound=list)
E = TypeVar("E")


def concat(*s: S | E) -> S:
    elems = []
    for x in s:
        if x is None:
            continue
        elems.extend(x) if isinstance(x, list) else elems.append(x)
    return elems


def insert(s: S, elem: E | S, i: int = None) -> S:
    i = len(s) if i is None else i
    s[i:i + 1] = elem if isinstance(elem, list) else [elem]
    return s
