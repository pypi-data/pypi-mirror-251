from typing import TypeVar

T = TypeVar("T", bound=dict)


def not_zero(m: T) -> T:
    return {k: v for k, v in m if v}
