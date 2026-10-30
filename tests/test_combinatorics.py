"""Unit tests for src/combinatorics.py. (TEAM TO WRITE)"""
import math
import pytest
from src.combinatorics import (
    harmonic_mean_M,
    prob,
    cumulative_prob,
    prob_array,
    largest_N_with_float_omega
)


def test_log_space_matches_exact_integers():
    # compare prob(N,k) with exact math.comb(N,k)/2**N for several N and all k
    for N in [5, 10, 20]:
        total_states = 2**N
        for k in range(N + 1):
            exact_p = math.comb(N, k) / total_states
            approx_p = prob(N, k)
            assert pytest.approx(approx_p, abs=1e-12) == exact_p


def test_probabilities_sum_to_one():
    # cumulative_prob(N, 0, N) == 1
    for N in [10, 50, 100, 138]:
        c_prob = cumulative_prob(N, 0, N)
        assert pytest.approx(c_prob, abs=1e-9) == 1.0


def test_symmetry():
    # prob(N,k) == prob(N,N-k)
    N = 138
    for k in range(N // 2 + 1):
        assert pytest.approx(prob(N, k), abs=1e-12) == prob(N, N - k)


def test_harmonic_mean():
    # known example; zero digit handling
    digits_team = [14, 75, 92, 99]
    assert harmonic_mean_M(digits_team) == 38

    # Testing handling of zero digit (safely converted to 1)
    digits_with_zero = [0, 50]
    assert harmonic_mean_M(digits_with_zero) == 2


def test_invalid_input():
    # k out of range must raise ValueError
    N = 50
    with pytest.raises(ValueError):
        prob(N, -1)
    with pytest.raises(ValueError):
        prob(N, 51)

