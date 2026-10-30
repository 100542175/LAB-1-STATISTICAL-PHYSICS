"""Combinatorics of N coins: multiplicities and probabilities.  (TEAM TO IMPLEMENT)"""
from __future__ import annotations

from typing import Sequence


def harmonic_mean_M(digits: Sequence[int]) -> int:
    """Harmonic average of the last two NIA digits, rounded to an integer.

    Decide and document: rounding rule, what to do if a digit is 0.
    """
    raise NotImplementedError


def ln_omega(N: int, k: int) -> float:
    """ln Omega(N, k) with the log-gamma function (guidelines, Eq. 1)."""
    raise NotImplementedError


def prob(N: int, k: int) -> float:
    """P_k = Omega(N, k) / 2**N without overflow."""
    raise NotImplementedError


def cumulative_prob(N: int, k1: int, k2: int) -> float:
    """Sum of P_k for k1 <= k <= k2 (inclusive)."""
    raise NotImplementedError


def prob_array(N: int):
    """P_k for k = 0..N as a NumPy array (needed for the plots)."""
    raise NotImplementedError


def largest_N_with_float_omega() -> int:
    """Largest N for which Omega(N, N//2) still fits in a double (item 1d)."""
    raise NotImplementedError
