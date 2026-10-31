"""Unit tests for src/thermodynamics.py."""
import math

import pytest

from src.combinatorics import prob
from src.thermodynamics import (
    KB,
    delta_S_over_kB,
    expected_waiting_time,
    log10_waiting_time,
    gauss_prob,
    gauss_window_prob,
    likelihood_ratio,
    likelihood_ratios_item_i,
    ln_omega_small_k,
    large_N_summary,
)


def test_entropy_is_maximal_at_N_over_2():
    N = 138
    k_mid = N // 2
    for k in range(N + 1):
        assert delta_S_over_kB(N, k, k_mid) <= 1e-12


def test_delta_S_matches_exact_ratio():
    N = 138
    for k1, k2 in [(94, 69), (79, 69), (69, 20)]:
        exact = math.log(math.comb(N, k1) / math.comb(N, k2))
        assert pytest.approx(delta_S_over_kB(N, k1, k2), rel=1e-10) == exact


def test_delta_S_signs_of_items_e_f_g():
    N, k = 138, 69
    assert delta_S_over_kB(N, k + 25, k) < delta_S_over_kB(N, k + 10, k) < 0
    assert delta_S_over_kB(N, k, 20) > 0


def test_waiting_time_is_inverse_probability():
    N, k = 10, 5
    p_k = prob(N, k)
    assert pytest.approx(expected_waiting_time(N, k, 1.0), rel=1e-9) == 1.0 / p_k
    assert pytest.approx(expected_waiting_time(N, k, 4.0), rel=1e-9) == 1.0 / (4.0 * p_k)


def test_waiting_time_default_is_one_configuration_per_second():
    assert expected_waiting_time(20, 10) == expected_waiting_time(20, 10, 1.0)


def test_waiting_time_invalid_rate_and_overflow_safe_version():
    with pytest.raises(ValueError):
        expected_waiting_time(20, 10, 0.0)
    with pytest.raises(OverflowError):
        expected_waiting_time(5000, 8)                    # does not fit in a double
    assert log10_waiting_time(5000, 8) > 308              # but the log10 version works
    assert pytest.approx(log10_waiting_time(20, 10), rel=1e-12) == math.log10(
        expected_waiting_time(20, 10))


def test_gaussian_close_to_exact_near_peak():
    N = 1000
    exact_peak = prob(N, N // 2)
    assert pytest.approx(gauss_prob(float(N), 0.0), rel=1e-2) == exact_peak


def test_gaussian_window_close_to_exact():
    from src.combinatorics import cumulative_prob
    N = 138
    assert pytest.approx(gauss_window_prob(N, 10), abs=2e-3) == cumulative_prob(N, 59, 79)


def test_likelihood_ratio_symmetry():
    N, k_mid = 100, 50
    r_plus = likelihood_ratio(N, k_mid, k_mid + 10)
    r_minus = likelihood_ratio(N, k_mid, k_mid - 10)
    assert pytest.approx(r_plus, rel=1e-9) == r_minus


def test_item_i_both_readings():
    N, M = 138, 38
    r = likelihood_ratios_item_i(N, M)
    assert pytest.approx(r["N/2+10"], rel=1e-9) == r["N/2-10"]
    assert r["M-10"] is not None and r["M-10"] > r["M+10"] > 1.0   # M-10 is far from the peak
    assert pytest.approx(r["M+10"], rel=1e-9) == math.comb(N, N // 2) / math.comb(N, M + 10)


def test_item_i_guard_for_small_M():
    r = likelihood_ratios_item_i(103, 3)      # M - 10 < 0
    assert r["M-10"] is None
    assert r["M+10"] is not None


def test_small_k_formula_matches_exact():
    assert pytest.approx(ln_omega_small_k(10 ** 6, 8), rel=1e-12) == math.log(math.comb(10 ** 6, 8))


def test_large_N_summary():
    s = large_N_summary(1e23, M=38)
    assert s["N"] == 1e23
    assert pytest.approx(s["relative_width"], rel=1e-3) == 3.162e-12      # sigma/mu
    assert pytest.approx(s["sigma_over_N"], rel=1e-3) == 1.581e-12
    assert s["relative_width"] < 1e-11
    assert s["S_max_over_kB"] > 1e22
    assert pytest.approx(s["dP_1sigma"], abs=1e-3) == 0.6827
    assert pytest.approx(s["dS_g_J_per_K"], abs=0.01) == 0.957           # ~ N kB ln 2
    assert s["dP_10"] < 1e-9 and s["dP_20"] < 1e-9                        # fixed windows -> 0
    assert abs(s["dS_e_over_kB"]) < 1e-19 and abs(s["dS_f_over_kB"]) < 1e-19
    assert s["log10_waiting_time_s"] > 1e22
    assert s["log10_ratio_M_minus_10"] > 1e22 and s["log10_ratio_M_plus_10"] > 1e22


def test_KB_value():
    assert KB == 1.380649e-23