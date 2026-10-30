"""Enumeration of the 2**N microstates.  (TEAM TO IMPLEMENT)

Guidelines: bitwise shifting (1 << N) and generators (yield); measure time and RAM.
"""
from __future__ import annotations

from typing import Iterator


def iter_microstates(N: int) -> Iterator[int]:
    """Generator over all 2**N microstates, encoded as integers."""
    raise NotImplementedError


def to_string(s: int, N: int) -> str:
    """Integer -> 'HHTHT...' string."""
    raise NotImplementedError


def count_heads(s: int) -> int:
    """Number of heads of a microstate."""
    raise NotImplementedError


def macrostate_counts(N: int) -> list[int]:
    """Omega(N, k) for k = 0..N obtained by visiting every microstate."""
    raise NotImplementedError


def microstates_by_macrostate(N: int) -> dict[int, list[str]]:
    """All microstate strings grouped by number of heads (small N only)."""
    raise NotImplementedError


def benchmark(func, N: int, repeats: int = 3) -> tuple[float, float]:
    """Mean and standard deviation of the wall-clock time of func(N)."""
    raise NotImplementedError


def peak_memory_bytes(func, N: int) -> int:
    """Peak memory used while running func(N)."""
    raise NotImplementedError
