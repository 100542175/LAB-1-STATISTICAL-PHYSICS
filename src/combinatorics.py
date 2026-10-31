"""Combinatorics of N coins: multiplicities and probabilities."""
from __future__ import annotations

import math
from typing import Sequence

import numpy as np
from scipy.special import gammaln


def harmonic_mean_M(digits: Sequence[int]) -> int:
    """Harmonic average of the last two NIA digits, rounded to an integer.

    Design decision (document it in the report): a digit equal to 0 would make
    the harmonic mean undefined, so it is replaced by 1. Negative values or an
    empty list are rejected.
    """
    if len(digits) == 0:
        raise ValueError("At least one NIA value is required.")
    if any(d < 0 for d in digits):
        raise ValueError("NIA digits must be non-negative.")
    cleaned_digits = [d if d != 0 else 1 for d in digits]
    n = len(cleaned_digits)
    h_mean = n / sum(1.0 / d for d in cleaned_digits)
    return round(h_mean)


def ln_omega(N: int, k: int) -> float:
    """ln Omega(N, k) with the log-gamma function (guidelines, Eq. 1)."""
    if k < 0 or k > N:
        raise ValueError(f"k must be between 0 and {N}, got {k}")
    return math.lgamma(N + 1) - math.lgamma(k + 1) - math.lgamma(N - k + 1)


def prob(N: int, k: int) -> float:
    """P_k = Omega(N, k) / 2**N without overflow using log-space computation."""
    if k < 0 or k > N:
        raise ValueError(f"k must be in range [0, {N}], got {k}")
    ln_p = ln_omega(N, k) - N * math.log(2)
    return math.exp(ln_p)


def cumulative_prob(N: int, k1: int, k2: int) -> float:
    """Sum of P_k for k1 <= k <= k2 (inclusive).

    Raises ValueError if k1 > k2 or if a limit lies outside [0, N].
    """
    if k1 > k2:
        raise ValueError(f"k1 must not exceed k2 (got {k1} > {k2})")
    if k1 < 0 or k2 > N:
        raise ValueError(f"limits must lie in [0, {N}], got [{k1}, {k2}]")
    return math.fsum(prob(N, k) for k in range(k1, k2 + 1))


def prob_array(N: int) -> np.ndarray:
    """P_k for k = 0..N as a NumPy array (vectorised, fast also for huge N)."""
    k = np.arange(N + 1, dtype=np.float64)
    ln_p = gammaln(N + 1.0) - gammaln(k + 1.0) - gammaln(N - k + 1.0) - N * math.log(2)
    return np.exp(ln_p)


def largest_N_with_float_omega() -> int:
    """Largest N for which Omega(N, N//2) still fits in a double (item 1d)."""
    N = 1
    while True:
        try:
            float(math.comb(N, N // 2))   # OverflowError when > ~1.8e308
            N += 1
        except OverflowError:
            return N - 1


def print_probability_report(digits: Sequence[int]):
    """Prints formatted summary of items 2a-2d."""
    M = harmonic_mean_M(digits)
    N = 100 + M
    if N >= 200:
        raise ValueError(f"N = {N} must be below 200; check the NIA digits.")

    P_a = prob(N, 30)
    k_b = N // 2
    P_b = prob(N, k_b)

    k1_c, k2_c = k_b - 10, k_b + 10
    delta_P_c = cumulative_prob(N, k1_c, k2_c)

    # Item d) is stated in TAILS; by the symmetry Omega(N,k) = Omega(N,N-k)
    # the range N/2 -+ 20 tails equals N/2 -+ 20 heads.
    k1_d, k2_d = k_b - 20, k_b + 20
    delta_P_d = cumulative_prob(N, k1_d, k2_d)

    print("\n" + "=" * 65)
    print(f" SECTION 4.1: PROBABILITY CALCULATIONS (N = {N})")
    print("=" * 65)
    print(f"Team Digits: {digits} | M = {M} | N = {N}")
    if N % 2:
        print(f"(N odd: N/2 is taken as floor(N/2) = {k_b})")
    print("-" * 65)
    print(f"a) P(k = 30 heads)        = {P_a:.6e}")
    print(f"b) P(k = N/2 = {k_b} heads)  = {P_b:.6f} ({P_b * 100:.2f}%)")
    print(f"c) ΔP (N/2 ± 10 heads)   = {delta_P_c:.6f} ({delta_P_c * 100:.2f}%)")
    print(f"d) ΔP (N/2 ± 20 tails)   = {delta_P_d:.6f} ({delta_P_d * 100:.2f}%)")
    print(f"   check: sum of all P_k - 1 = {cumulative_prob(N, 0, N) - 1.0:.1e}")
    print("=" * 65 + "\n")