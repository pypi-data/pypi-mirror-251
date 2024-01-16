from typing import TypeVar

T = TypeVar("T", bound=dict)


def not_zero(m: T) -> T:
    return {k: v for k, v in m if v}


def diff(m1: dict, m2: dict, key=True) -> dict:
    if key:
        return {k: v for k, v in m1.items() if k not in m2}
    return {k: v for k, v in m1.items() if v != m2.get(k, None)}


def diff_key(m1: dict, m2: dict) -> dict:
    return [k for k, v in m1.items() if v != m2.get(k, None)]


def diff_value(m1: dict, m2: dict) -> dict:
    return [v for k, v in m1.items() if v != m2.get(k, None)]
