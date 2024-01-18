from typing import TypeVar

M = TypeVar("M", bound=dict)


def nonzero(m: M) -> M:
    return {k: v for k, v in m if v}


def diff(m1: M, m2: M, key=True) -> M:
    return {
        k: v for k, v in m1.items()
        if key and k not in m2 or v != m2.get(k, None)
    }


def diff_key(m1: M, m2: M) -> M:
    return [k for k, v in m1.items() if v != m2.get(k, None)]


def diff_value(m1: M, m2: M) -> M:
    return [v for k, v in m1.items() if v != m2.get(k, None)]
