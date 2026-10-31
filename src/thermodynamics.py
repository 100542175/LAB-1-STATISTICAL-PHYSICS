"""Entropy, waiting times and the large-N limit."""
from __future__ import annotations

import math

from src.combinatorics import ln_omega

KB: float = 1.380649e-23            # J/K
YEAR_S: float = 365.25 * 86400.0    # seconds per (Julian) year
AGE_UNIVERSE_S: float = 13.8e9 * YEAR_S


# ----------------------------------------------------------------- exact (finite N)
def delta_S_over_kB(N: int, k1: int, k2: int) -> float:
    """(S(k1) - S(k2)) / k_B, with S = k_B ln Omega."""
    return ln_omega(N, k1) - ln_omega(N, k2)


def log10_waiting_time(N: int, k: int, configs_per_second: float = 1.0) -> float:
    """log10 of the expected waiting time (s) to obtain exactly k heads.

    Safe for any N (no overflow). Each toss of the N coins is one trial with
    success probability P_k, so the mean number of trials is 1/P_k.
    """
    if configs_per_second <= 0:
        raise ValueError("configs_per_second must be positive")
    ln_t = N * math.log(2) - ln_omega(N, k) - math.log(configs_per_second)
    return ln_t / math.log(10)


def expected_waiting_time(N: int, k: int, configs_per_second: float = 1.0) -> float:
    """Expected time (s) to obtain exactly k heads.

    Assumption (state it in the report): "a tossing rate of N coins per second"
    = all N coins are tossed once per second = 1 configuration per second, hence
    the default configs_per_second = 1. Raises OverflowError if the time does not
    fit in a double; use log10_waiting_time in that case.
    """
    if configs_per_second <= 0:
        raise ValueError("configs_per_second must be positive")
    ln_t = N * math.log(2) - ln_omega(N, k) - math.log(configs_per_second)
    return math.exp(ln_t)


def likelihood_ratio(N: int, k_a: int, k_b: int) -> float:
    """P(k_a) / P(k_b) calculated via log-space differences."""
    ln_ratio = ln_omega(N, k_a) - ln_omega(N, k_b)
    return math.exp(ln_ratio)


def likelihood_ratios_item_i(N: int, M: int) -> dict[str, float | None]:
    """Item 2i under both readings of 'M-not-+-10 heads' (ask the instructor).

    Reading A: macrostates N/2 +- 10 heads (symmetric, always defined).
    Reading B: literally M + 10 and M - 10 heads; None if k is outside [0, N].
    """
    k_peak = N // 2

    def ratio(k: int) -> float | None:
        return likelihood_ratio(N, k_peak, k) if 0 <= k <= N else None

    return {
        "N/2+10": ratio(k_peak + 10),
        "N/2-10": ratio(k_peak - 10),
        "M+10": ratio(M + 10),
        "M-10": ratio(M - 10),
    }


# ----------------------------------------------------------------- Gaussian / large N
def sigma(N: float) -> float:
    """Standard deviation of the number of heads: sqrt(N)/2."""
    return math.sqrt(N) / 2.0


def relative_width(N: float) -> float:
    """sigma / mu with mu = N/2:  1/sqrt(N)."""
    return 1.0 / math.sqrt(N)


def gauss_prob(N: float, x: float) -> float:
    """Gaussian approximation of P(k = N/2 + x) in the large-N limit.

    P(x) approx sqrt(2 / (pi * N)) * exp(-2 * x^2 / N)
    """
    return math.sqrt(2.0 / (math.pi * N)) * math.exp(-2.0 * (x ** 2) / N)


def gauss_window_prob(N: float, half_width: float) -> float:
    """P(|k - N/2| <= half_width), Gaussian with continuity correction."""
    return math.erf((half_width + 0.5) * math.sqrt(2.0 / N))


def ln_omega_small_k(N: float, k: int) -> float:
    """ln C(N, k) for huge N and small integer k, without cancellation.

    ln C(N,k) = sum_{j=0}^{k-1} ln[(N - j)/(k - j)]. (A difference of two
    lgamma values at N ~ 1e23 would lose every significant digit.)
    """
    return sum(math.log((N - j) / (k - j)) for j in range(k))


def large_N_summary(N: float = 1e23, M: int | None = None) -> dict[str, float]:
    """Items 2a-2i re-evaluated for N ~ 1e23 (analytic, Gaussian/Stirling).

    If M is given, the literal 'M +- 10 heads' reading of item i is added.
    """
    ln2 = math.log(2.0)
    ln10 = math.log(10.0)
    s = sigma(N)
    ln_center = N * ln2 + 0.5 * math.log(2.0 / (math.pi * N))   # ln Omega(N, N/2)
    dS_g = ln_center - ln_omega_small_k(N, 20)

    out = {
        "N": N,
        "sigma": s,
        "relative_width": relative_width(N),          # sigma/mu = 1/sqrt(N)
        "sigma_over_N": s / N,                        # = 1/(2 sqrt(N))
        "peak_probability": gauss_prob(N, 0.0),
        "p_displacement_1e10": gauss_prob(N, 1e10),
        "log10_P30": (ln_omega_small_k(N, 30) - N * ln2) / ln10,      # item a
        "dP_10": gauss_window_prob(N, 10),                            # item c
        "dP_20": gauss_window_prob(N, 20),                            # item d
        "dP_1sigma": gauss_window_prob(N, s),
        "dP_5sigma_complement": 1.0 - gauss_window_prob(N, 5 * s),
        "dS_e_over_kB": -2.0 * 25.0 ** 2 / N,                         # item e
        "dS_f_over_kB": -2.0 * 10.0 ** 2 / N,                         # item f
        "dS_g_over_kB": dS_g,                                         # item g
        "dS_g_J_per_K": KB * dS_g,
        "S_max_over_kB": N * ln2,
        "log10_waiting_time_s": (N * ln2 - ln_omega_small_k(N, 8)) / ln10,   # item h
        "ratio_minus_1": math.expm1(2.0 * 10.0 ** 2 / N),             # item i, N/2 +- 10
    }
    out["log10_waiting_time_years"] = out["log10_waiting_time_s"] - math.log10(YEAR_S)
    if M is not None:                                                  # item i, literal reading
        for sign, name in ((+1, "plus"), (-1, "minus")):
            k = M + sign * 10
            if k >= 0:
                out[f"log10_ratio_M_{name}_10"] = (ln_center - ln_omega_small_k(N, k)) / ln10
    return out


# ----------------------------------------------------------------- report
def print_thermodynamics_report(digits: list[int]):
    """Prints formatted summary covering Sections 2e through 2k."""
    from src.combinatorics import harmonic_mean_M, prob

    M = harmonic_mean_M(digits)
    N = 100 + M
    k_peak = N // 2

    # 2e - 2g: Entropy changes
    dS_e = delta_S_over_kB(N, k_peak + 25, k_peak)
    dS_f = delta_S_over_kB(N, k_peak + 10, k_peak)
    dS_g = delta_S_over_kB(N, k_peak, 20)

    # 2h: waiting time for k = 8 heads (1 configuration per second)
    t_sec = expected_waiting_time(N, 8, configs_per_second=1.0)
    t_years = t_sec / YEAR_S

    # 2i: likelihood ratios under both readings
    ratios = likelihood_ratios_item_i(N, M)

    # Extra check (NOT item j): Gaussian vs exact peak
    p_exact_peak = prob(N, k_peak)
    p_gauss_peak = gauss_prob(float(N), 0.0)
    rel_error = abs(p_exact_peak - p_gauss_peak) / p_exact_peak * 100.0

    L = large_N_summary(1e23, M=M)

    def fmt(r):
        return "undefined (k outside [0, N])" if r is None else f"{r:.4e}"

    print("\n" + "=" * 65)
    print(f" SECTIONS 2e-2k: THERMODYNAMICS & LARGE-N LIMIT (N = {N})")
    print("=" * 65)
    print(f"e) ΔS/k_B (k1 = N/2+25 vs k2 = N/2)  = {dS_e:.6f}")
    print(f"f) ΔS/k_B (k1 = N/2+10 vs k2 = N/2)  = {dS_f:.6f}")
    print(f"g) ΔS/k_B (k1 = N/2 vs k2 = 20)      = {dS_g:.6f}   ({KB * dS_g:.3e} J/K)")
    print("-" * 65)
    print("h) Waiting time for k = 8 heads (1 configuration/s, i.e. N coins/s):")
    print(f"   t = {t_sec:.6e} s = {t_years:.6e} years = {t_sec / AGE_UNIVERSE_S:.2e} x age of universe")
    print("i) Likelihood ratios P(N/2)/P(k):")
    print(f"   reading A, k = N/2+10 : {fmt(ratios['N/2+10'])}   k = N/2-10 : {fmt(ratios['N/2-10'])}")
    print(f"   reading B, k = M+10   : {fmt(ratios['M+10'])}   k = M-10   : {fmt(ratios['M-10'])}")
    print("j) Second Law: written discussion required in the report (no number).")
    print("-" * 65)
    print(f"extra) Gaussian validation (N = {N}): exact P_peak = {p_exact_peak:.6f}, "
          f"Gauss = {p_gauss_peak:.6f}, rel. error = {rel_error:.2f}%")
    print("-" * 65)
    print("k) Items a-i for N = 1e23 (analytic):")
    print(f"   sigma = {L['sigma']:.3e} heads;  sigma/mu = {L['relative_width']:.3e};  sigma/N = {L['sigma_over_N']:.3e}")
    print(f"   a) log10 P(30)            = {L['log10_P30']:.3e}")
    print(f"   b) P(N/2)                 = {L['peak_probability']:.3e}")
    print(f"   c) dP(N/2 ± 10)           = {L['dP_10']:.3e}")
    print(f"   d) dP(N/2 ± 20)           = {L['dP_20']:.3e}   (window ±sigma: {100 * L['dP_1sigma']:.1f} %)")
    print(f"   e) ΔS/k_B                 = {L['dS_e_over_kB']:.3e}")
    print(f"   f) ΔS/k_B                 = {L['dS_f_over_kB']:.3e}")
    print(f"   g) ΔS/k_B                 = {L['dS_g_over_kB']:.3e}  ({L['dS_g_J_per_K']:.3f} J/K)")
    print(f"   h) log10 t (s)            = {L['log10_waiting_time_s']:.3e}")
    print(f"   i) ratio - 1 (N/2 ± 10)   = {L['ratio_minus_1']:.3e}")
    print("=" * 65 + "\n")