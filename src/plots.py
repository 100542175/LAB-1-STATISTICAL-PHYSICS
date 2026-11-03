"""Vector (PDF) figures for the report.

Plot functions only draw: measurements (timings) are taken elsewhere
(src.microstates.measure_enumeration) and passed in.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")                      # works without a display (CI, servers)
import matplotlib.pyplot as plt            # noqa: E402
import numpy as np                         # noqa: E402

from src.combinatorics import harmonic_mean_M, ln_omega, prob, prob_array   # noqa: E402
from src.microstates import extrapolate_max_N, measure_enumeration           # noqa: E402

DISTRIBUTION_NS = [20, 50, 80, 100]        # item 1c of the manual
BUDGET_S = 300.0                           # five minutes


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, format="pdf" if path.suffix == ".pdf" else None)
    plt.close(fig)


def figure_distributions(Ns: list[int], path: Path) -> None:
    """Item 1c: macrostate distribution versus k for all N in one figure.

    Left: probability P_k = Omega/2^N (linear). Right: multiplicity Omega(N,k)
    (log scale), the quantity asked for in the manual.
    """
    fig, (ax_p, ax_o) = plt.subplots(1, 2, figsize=(10, 4.2))
    for N in Ns:
        k = np.arange(N + 1)
        ax_p.plot(k, prob_array(N), marker="o", markersize=2.5, linewidth=1.2,
                  label=f"$N = {N}$")
        omega = np.exp([ln_omega(N, int(kk)) for kk in k])       # exact to ~1e-13
        ax_o.plot(k, omega, marker="o", markersize=2.5, linewidth=1.2,
                  label=f"$N = {N}$")

    ax_p.set_title("Probability $P_k=\\Omega(N,k)/2^N$", fontsize=11)
    ax_p.set_xlabel("Number of heads $k$ [dimensionless]")
    ax_p.set_ylabel("$P_k$ [dimensionless]")
    ax_p.set_xlim(left=0)
    ax_p.set_ylim(bottom=0)
    ax_o.set_title("Multiplicity $\\Omega(N,k)$", fontsize=11)
    ax_o.set_xlabel("Number of heads $k$ [dimensionless]")
    ax_o.set_ylabel("$\\Omega(N,k)$ [number of microstates]")
    ax_o.set_yscale("log")
    ax_o.set_xlim(left=0)
    for ax in (ax_p, ax_o):
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(loc="best", frameon=True)
    _save(fig, path)


def figure_probabilities(N: int, k0: int, path: Path) -> None:
    """Item 2: P_k for the team's N with the +-10 / +-20 windows and k = 30 marked."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    k = np.arange(N + 1)
    ax.plot(k, prob_array(N), color="#2b5c8f", linewidth=1.5, label=f"$P_k$ for $N = {N}$")

    ax.axvline(k0, color="black", linestyle="--", linewidth=1.2,
               label=f"Peak $k_0 = {k0}$ ($P={prob(N, k0):.4f}$)")
    if 0 <= 30 <= N:
        ax.axvline(30, color="#7570b3", linestyle=":", linewidth=1.5,
                   label=f"$k = 30$ ($P={prob(N, 30):.2e}$)")
    if k0 - 10 >= 0 and k0 + 10 <= N:
        ax.axvspan(k0 - 10, k0 + 10, color="#2b5c8f", alpha=0.2, label="$k_0 \\pm 10$ window")
    if k0 - 20 >= 0 and k0 + 20 <= N:
        ax.axvspan(k0 - 20, k0 + 20, color="#d95f02", alpha=0.1, label="$k_0 \\pm 20$ window")

    ax.set_title(f"Macrostate probability distribution ($N = {N}$)", fontsize=12)
    ax.set_xlabel("Number of heads $k$ [dimensionless]")
    ax.set_ylabel("Probability $P_k$ [dimensionless]")
    ax.set_xlim(0, N)
    ax.set_ylim(bottom=0)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", frameon=True, fontsize=8)
    _save(fig, path)


def figure_timing(data: list[tuple[int, float, float]], path: Path,
                  budget_s: float = BUDGET_S) -> int:
    """Item 1b: measured enumeration time versus N (mean +- std, log scale).

    data: [(N, mean_s, std_s), ...] from src.microstates.measure_enumeration.
    Draws the 2^N extrapolation from the last point and the five-minute limit.
    Returns the extrapolated largest N that fits in budget_s.
    """
    if len(data) < 2:
        raise ValueError("At least two (N, mean, std) points are required.")
    Ns = np.array([d[0] for d in data], dtype=float)
    means = np.array([d[1] for d in data])
    stds = np.array([d[2] for d in data])
    N_last, t_last = int(Ns[-1]), float(means[-1])
    N_max = extrapolate_max_N(N_last, t_last, budget_s)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.errorbar(Ns, means, yerr=stds, fmt="o-", color="#e7298a", linewidth=1.8,
                markersize=5, capsize=3, label="measured (mean $\\pm$ std)")
    n_ref = np.linspace(Ns[0], N_max + 1, 100)
    ax.plot(n_ref, t_last * 2.0 ** (n_ref - N_last), "k--", linewidth=1,
            label="$\\propto 2^N$ extrapolation")
    ax.axhline(budget_s, color="red", linewidth=1)
    ax.text(n_ref[-1], budget_s * 1.4, "5 minutes", color="red", ha="right")
    ax.axvline(N_max, color="gray", linestyle=":", linewidth=1,
               label=f"extrapolated $N_{{max}} = {N_max}$")

    ax.set_yscale("log")
    ax.set_title("Full microstate enumeration: wall-clock time vs. $N$", fontsize=12)
    ax.set_xlabel("System size $N$ [coins]")
    ax.set_ylabel("Wall-clock time [seconds]")
    ax.grid(True, which="both", linestyle=":", alpha=0.6)
    ax.legend(loc="lower right", frameon=True, fontsize=8)
    _save(fig, path)
    return N_max


def generate_all_figures(digits: list[int], out_dir: Path = Path("report/figures"),
                         timing_data: list[tuple[int, float, float]] | None = None) -> int:
    """Generate every vector figure of the report. Returns the extrapolated N_max.

    timing_data: pass the result of measure_enumeration; if None, a short default
    measurement (N = 10..20) is taken here.
    """
    M = harmonic_mean_M(digits)
    N = 100 + M
    k0 = N // 2
    if timing_data is None:
        timing_data = measure_enumeration(list(range(10, 21, 2)), repeats=3)

    figure_distributions(DISTRIBUTION_NS, out_dir / "figure_distributions.pdf")
    figure_probabilities(N, k0, out_dir / "figure_probabilities.pdf")
    return figure_timing(timing_data, out_dir / "figure_timing.pdf")
