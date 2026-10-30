"""Unit tests for src/combinatorics.py. (TEAM TO WRITE)"""
import pytest

def test_log_space_matches_exact_integers():
    # compare prob(N,k) with exact math.comb(N,k)/2**N for several N and all k
    pytest.skip("TODO")

def test_probabilities_sum_to_one():
    # cumulative_prob(N, 0, N) == 1
    pytest.skip("TODO")

def test_symmetry():
    # prob(N,k) == prob(N,N-k)
    pytest.skip("TODO")

def test_harmonic_mean():
    # known example; zero digit handling
    pytest.skip("TODO")

def test_invalid_input():
    # k out of range must raise ValueError
    pytest.skip("TODO")

