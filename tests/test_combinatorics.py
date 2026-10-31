"""Unit tests for src/combinatorics.py."""
import math

import numpy as np
import pytest

from src.combinatorics import (
    harmonic_mean_M,
    prob,
    cumulative_prob,
    prob_array,
    largest_N_with_float_omega,
)


def test_log_space_matches_exact_integers():
    # relative tolerance: absolute-only tolerances hide errors in tiny probabilities
    for N in [5, 10, 20, 100, 138, 199]:
        total_states = 2 ** N
        for k in range(N + 1):
            exact_p = math.comb(N, k) / total_states
            assert pytest.approx(prob(N, k), rel=1e-10) == exact_p


def test_probabilities_sum_to_one():
    for N in [10, 50, 100, 138, 199]:
        assert pytest.approx(cumulative_prob(N, 0, N), abs=1e-12) == 1.0


def test_symmetry():
    N = 138
    for k in range(N // 2 + 1):
        assert pytest.approx(prob(N, k), rel=1e-10) == prob(N, N - k)


def test_cumulative_matches_exact_sum():
    N, k1, k2 = 138, 59, 79
    exact = sum(math.comb(N, k) for k in range(k1, k2 + 1)) / 2 ** N
    assert pytest.approx(cumulative_prob(N, k1, k2), rel=1e-10) == exact


def test_cumulative_invalid_limits():
    with pytest.raises(ValueError):
        cumulative_prob(50, 30, 20)      # k1 > k2
    with pytest.raises(ValueError):
        cumulative_prob(50, -1, 10)
    with pytest.raises(ValueError):
        cumulative_prob(50, 10, 51)


def test_prob_array_matches_scalar():
    N = 138
    arr = prob_array(N)
    assert arr.shape == (N + 1,)
    ref = np.array([prob(N, k) for k in range(N + 1)])
    assert np.allclose(arr, ref, rtol=1e-10, atol=0.0)
    assert pytest.approx(arr.sum(), abs=1e-12) == 1.0


def test_largest_N_with_float_omega():
    n = largest_N_with_float_omega()
    assert n == 1029
    float(math.comb(n, n // 2))                  # still fits
    with pytest.raises(OverflowError):
        float(math.comb(n + 1, (n + 1) // 2))    # no longer fits


def test_harmonic_mean():
    digits_team = [14, 75, 92, 99]
    assert harmonic_mean_M(digits_team) == 38
    assert harmonic_mean_M([10, 10, 10, 10]) == 10

    # a zero digit is replaced by 1 (documented design decision)
    assert harmonic_mean_M([0, 50]) == 2
    assert harmonic_mean_M([0, 50]) == harmonic_mean_M([1, 50])


def test_harmonic_mean_invalid():
    with pytest.raises(ValueError):
        harmonic_mean_M([])
    with pytest.raises(ValueError):
        harmonic_mean_M([-5, 20])


def test_invalid_input():
    N = 50
    with pytest.raises(ValueError):
        prob(N, -1)
    with pytest.raises(ValueError):
        prob(N, 51)

