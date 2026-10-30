"""Unit tests for src/thermodynamics.py. (TEAM TO WRITE)"""
import math
import pytest
from src.combinatorics import prob
from src.thermodynamics import (
    delta_S_over_kB,
    expected_waiting_time,
    gauss_prob,
    likelihood_ratio,
    large_N_summary,
)


def test_entropy_is_maximal_at_N_over_2():
    # delta_S_over_kB(N, k, N//2) <= 0 because N//2 is maximum multiplicity
    N = 138
    k_mid = N // 2
    for k in [10, 28, 48, k_mid + 10]:
        assert delta_S_over_kB(N, k, k_mid) <= 0.0


def test_waiting_time_is_inverse_probability():
    # small N check: t = 1 / (rate * P_k)
    N = 10
    k = 5
    p_k = prob(N, k)
    rate = 1.0
    expected_t = 1.0 / (rate * p_k)
    assert pytest.approx(expected_waiting_time(N, k, rate), rel=1e-9) == expected_t


def test_gaussian_close_to_exact_near_peak():
    # N = 1000, compare exact peak prob vs Gauss peak prob (x=0)
    N = 1000
    k_mid = N // 2
    exact_peak = prob(N, k_mid)
    gauss_peak = gauss_prob(float(N), 0.0)
    assert pytest.approx(gauss_peak, rel=1e-2) == exact_peak


def test_likelihood_ratio_symmetry():
    # For symmetric distances from N//2, ratio should be equal for even N
    N = 100
    k_mid = 50
    ratio_plus = likelihood_ratio(N, k_mid, k_mid + 10)
    ratio_minus = likelihood_ratio(N, k_mid, k_mid - 10)
    assert pytest.approx(ratio_plus, rel=1e-9) == ratio_minus


def test_large_N_summary():
    summary = large_N_summary(1e23)
    assert summary["N"] == 1e23
    assert summary["relative_width"] < 1e-11
    assert summary["S_max_over_kB"] > 1e22

