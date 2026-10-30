"""Entropy, waiting times and the large-N limit.  (TEAM TO IMPLEMENT)"""
from __future__ import annotations

KB: float = 1.380649e-23  # J/K


def delta_S_over_kB(N: int, k1: int, k2: int) -> float:
    """(S(k1) - S(k2)) / k_B, with S = k_B ln Omega."""
    raise NotImplementedError


def expected_waiting_time(N: int, k: int, configs_per_second: float = 1.0) -> float:
    """Expected time (s) to obtain exactly k heads. State your assumption (item 2h)."""
    raise NotImplementedError


def likelihood_ratio(N: int, k_a: int, k_b: int) -> float:
    """P(k_a) / P(k_b) (item 2i)."""
    raise NotImplementedError


def gauss_prob(N: float, x: float) -> float:
    """Gaussian approximation of P(k = N/2 + x) (items 1e and 2k)."""
    raise NotImplementedError


def large_N_summary(N: float = 1e23) -> dict[str, float]:
    """Items 2a-2i evaluated for N ~ 1e23 (analytic; beware of cancellation)."""
    raise NotImplementedError
