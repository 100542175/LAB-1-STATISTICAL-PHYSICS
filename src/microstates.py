"""Enumeration of the 2**N microstates.

A microstate is an integer s in [0, 2**N): bit i = 1 means coin i is heads.
"""
from __future__ import annotations

import math
import time
import tracemalloc
from typing import Callable, Iterator


def iter_microstates(N: int) -> Iterator[int]:
    """Generator over all 2**N microstates, encoded as integers from 0 to 2**N - 1."""
    if N < 0:
        raise ValueError(f"N must be non-negative, got {N}")
    for state in range(1 << N):      # bitwise shift: 1 << N == 2**N
        yield state


def to_string(s: int, N: int) -> str:
    """Integer -> 'HHTHT...' string (most significant bit first)."""
    if N < 0:
        raise ValueError(f"N must be non-negative, got {N}")
    if N == 0:
        if s != 0:
            raise ValueError(f"State {s} out of bounds for N=0")
        return ""
    if s < 0 or s >= (1 << N):
        raise ValueError(f"State {s} out of bounds for N={N}")
    bits = format(s, f"0{N}b")
    return bits.replace("1", "H").replace("0", "T")


def count_heads(s: int) -> int:
    """Number of heads (set bits) of an integer-encoded microstate."""
    if s < 0:
        raise ValueError("State must be non-negative")
    return s.bit_count()             # population count (Python >= 3.10)


def macrostate_counts(N: int) -> list[int]:
    """Omega(N, k) for k = 0..N obtained by visiting every microstate."""
    counts = [0] * (N + 1)
    for state in iter_microstates(N):
        counts[count_heads(state)] += 1
    return counts


def microstates_by_macrostate(N: int) -> dict[int, list[str]]:
    """All microstate strings grouped by number of heads k (small N only)."""
    grouped: dict[int, list[str]] = {k: [] for k in range(N + 1)}
    for state in iter_microstates(N):
        grouped[count_heads(state)].append(to_string(state, N))
    return grouped


# ------------------------------------------------------------------ performance (item 1b)
def benchmark(func: Callable[[int], object], N: int, repeats: int = 3) -> tuple[float, float]:
    """Mean and sample standard deviation (ddof = 1) of the wall-clock time of func(N).

    With a single repeat the standard deviation is reported as 0.0.
    """
    if repeats < 1:
        raise ValueError("repeats must be >= 1")
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        func(N)
        times.append(time.perf_counter() - start)
    mean_time = sum(times) / repeats
    if repeats == 1:
        return mean_time, 0.0
    variance = sum((t - mean_time) ** 2 for t in times) / (repeats - 1)
    return mean_time, math.sqrt(variance)


def peak_memory_bytes(func: Callable[[int], object], N: int) -> int:
    """Peak memory in bytes allocated while executing func(N).

    tracemalloc slows Python loops a lot: measure memory in a separate run from
    the timing, and at a modest N (for the generator it does not depend on N).
    """
    tracemalloc.start()
    try:
        func(N)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return peak


def measure_enumeration(Ns: list[int], repeats: int = 3,
                        func: Callable[[int], object] = macrostate_counts
                        ) -> list[tuple[int, float, float]]:
    """Time the full enumeration for each N. Returns [(N, mean_s, std_s), ...]."""
    return [(n, *benchmark(func, n, repeats)) for n in Ns]


def extrapolate_max_N(N_last: int, t_last: float, budget_s: float = 300.0) -> int:
    """Largest N whose enumeration fits in budget_s, assuming t doubles per +1 in N."""
    if t_last <= 0 or budget_s <= 0:
        raise ValueError("t_last and budget_s must be positive")
    if t_last > budget_s:
        return N_last - int(math.ceil(math.log2(t_last / budget_s)))
    return N_last + int(math.floor(math.log2(budget_s / t_last)))


# ------------------------------------------------------------------ item 1a
def n7_table_rows(N: int = 7) -> list[tuple[int, int, float]]:
    """[(k, Omega(N,k), P_k)] from k = N down to 0, using the enumeration."""
    grouped = microstates_by_macrostate(N)
    total = 1 << N
    return [(k, len(grouped[k]), len(grouped[k]) / total) for k in range(N, -1, -1)]


def n7_listing_lines(N: int = 7) -> list[str]:
    """One line per macrostate with ALL its microstates (like Table 1 of the manual)."""
    grouped = microstates_by_macrostate(N)
    lines = []
    for k in range(N, -1, -1):
        lines.append(f"{k} heads and {N - k} tails (Omega = {len(grouped[k])}): "
                     + ", ".join(grouped[k]))
    return lines


def print_n7_table(show_microstates: bool = True) -> None:
    """Prints the multiplicity table for N = 7 and, optionally, every microstate."""
    N = 7
    total_states = 1 << N

    print("\n" + "=" * 65)
    print(f" SECTION 1a: MICROSTATE ENUMERATION FOR N = {N} COINS")
    print("=" * 65)
    print(f"{'k (Heads)':<10} {'Multiplicity Omega(7,k)':<25} {'Probability P(k)':<18}")
    print("-" * 65)
    for k, omega, p_k in n7_table_rows(N):
        print(f"{k:<10} {omega:<25} {p_k:.6f} ({p_k * 100:.2f}%)")
    print("-" * 65)
    print(f"Total Microstates (2^7): {total_states} | Total Macrostates: {N + 1}")
    if show_microstates:
        print("-" * 65)
        for line in n7_listing_lines(N):
            print(line)
    print("=" * 65 + "\n")
