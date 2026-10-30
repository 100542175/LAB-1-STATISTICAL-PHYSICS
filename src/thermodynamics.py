"""Entropy, waiting times and the large-N limit.  (TEAM TO IMPLEMENT)"""
from __future__ import annotations

import math
from src.combinatorics import ln_omega

KB: float = 1.380649e-23  # J/K


def delta_S_over_kB(N: int, k1: int, k2: int) -> float:
    """(S(k1) - S(k2)) / k_B, with S = k_B ln Omega."""
    return ln_omega(N, k1) - ln_omega(N, k2)


def expected_waiting_time(N: int, k: int, configs_per_second: float = 1.0) -> float:
    """Expected time (s) to obtain exactly k heads.
    Assumption: Microstates are sampled at configs_per_second rate.
    Calculated via log-space to prevent float overflow:
    ln(t) = N * ln(2) - ln_omega(N, k) - ln(configs_per_second)
    """
    if configs_per_second <= 0:
        raise ValueError("configs_per_second must be positive")
    ln_t = N * math.log(2) - ln_omega(N, k) - math.log(configs_per_second)
    return math.exp(ln_t)


def likelihood_ratio(N: int, k_a: int, k_b: int) -> float:
    """P(k_a) / P(k_b) calculated via log-space differences."""
    ln_ratio = ln_omega(N, k_a) - ln_omega(N, k_b)
    return math.exp(ln_ratio)


def gauss_prob(N: float, x: float) -> float:
    """Gaussian approximation of P(k = N/2 + x) in the large-N limit.
    
    P(x) approx sqrt(2 / (pi * N)) * exp(-2 * x^2 / N)
    """
    return math.sqrt(2.0 / (math.pi * N)) * math.exp(-2.0 * (x**2) / N)


def large_N_summary(N: float = 1e23) -> dict[str, float]:
    """Items 2a-2i evaluated for N ~ 1e23 (analytic)."""
    peak_prob = gauss_prob(N, 0)
    p_disp = gauss_prob(N, 1e10)
    rel_width = 1.0 / (2.0 * math.sqrt(N))
    s_max_over_kb = N * math.log(2)
    
    return {
        "N": N,
        "peak_probability": peak_prob,
        "p_displacement_1e10": p_disp,
        "relative_width": rel_width,
        "S_max_over_kB": s_max_over_kb,
    }


def print_thermodynamics_report(digits: list[int]):
    """Prints formatted summary covering Sections 2e through 2k."""
    from src.combinatorics import harmonic_mean_M, prob
    
    M = harmonic_mean_M(digits)
    N = 100 + M
    k_peak = N // 2
    
    # 2e - 2g: Entropy Changes
    dS_e = delta_S_over_kB(N, k_peak + 25, k_peak)
    dS_f = delta_S_over_kB(N, k_peak + 10, k_peak)
    dS_g = delta_S_over_kB(N, k_peak, 20)
    
    # 2h: Waiting time for k = 8 heads
    t_sec = expected_waiting_time(N, 8, configs_per_second=float(N))
    t_years = t_sec / (365.25 * 86400)
    
    # 2i: Likelihood Ratios P(N/2) / P(M +/- 10)
    k_upper = M + 10
    k_lower = M - 10
    ratio_upper = likelihood_ratio(N, k_peak, k_upper)
    ratio_lower = likelihood_ratio(N, k_peak, k_lower)
    
    # 2j: Gaussian vs Exact Validation
    p_exact_peak = prob(N, k_peak)
    p_gauss_peak = gauss_prob(float(N), 0.0)
    rel_error = abs(p_exact_peak - p_gauss_peak) / p_exact_peak * 100.0
    
    # 2k: Large N Limit
    summary_2k = large_N_summary(1e23)
    
    print("\n" + "=" * 65)
    print(f" SECTIONS 2e-2k: THERMODYNAMICS & LARGE-N LIMIT (N = {N})")
    print("=" * 65)
    print(f"e) ΔS/k_B (k1 = N/2+25 vs k2 = N/2)  = {dS_e:.6f}")
    print(f"f) ΔS/k_B (k1 = N/2+10 vs k2 = N/2)  = {dS_f:.6f}")
    print(f"g) ΔS/k_B (k1 = N/2 vs k2 = 20)      = {dS_g:.6f}")
    print("-" * 65)
    print(f"h) Waiting time for k = 8 heads      = {t_sec:.6e} s ({t_years:.6e} years)")
    print(f"i) Likelihood Ratio P(N/2)/P(M+10)   = {ratio_upper:.4f}x")
    print(f"   Likelihood Ratio P(N/2)/P(M-10)   = {ratio_lower:.4e}x")
    print("-" * 65)
    print(f"j) Gaussian Validation (N = {N}):")
    print(f"   Exact P_peak = {p_exact_peak:.6f} | Gauss P_peak = {p_gauss_peak:.6f}")
    print(f"   Relative Error = {rel_error:.2f}%")
    print("-" * 65)
    print(f"k) Large N Limit (N = 10^23):")
    print(f"   Peak Probability P(N/2)          ~ {summary_2k['peak_probability']:.6e}")
    print(f"   Probability P(x = 10^10)         ~ {summary_2k['p_displacement_1e10']:.6e}")
    print(f"   Relative Fluctuation (σ/N)       ~ {summary_2k['relative_width']:.6e}")
    print(f"   Max Entropy S_max / k_B          ~ {summary_2k['S_max_over_kB']:.6e}")
    print("=" * 65 + "\n")