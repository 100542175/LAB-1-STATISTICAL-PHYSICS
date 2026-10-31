"""Vector (PDF) figures for the report. (TEAM TO IMPLEMENT)

Every axis needs a label with units ('dimensionless' counts), and the caption goes in LaTeX.
"""
from __future__ import annotations

import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.combinatorics import harmonic_mean_M, prob_array, prob


def figure_distributions(Ns: list[int], path: Path) -> None:
    """Item 1c: macrostate distribution versus k for all N in one figure."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

    for N in Ns:
        k = np.arange(N + 1)
        p_exact = prob_array(N)
        ax.plot(
            k,
            p_exact,
            marker="o" if N <= 15 else None,
            markersize=3,
            linewidth=1.8,
            label=f"$N = {N}$",
        )

    ax.set_title("Macrostate Probability Distributions for Various System Sizes $N$", fontsize=12)
    ax.set_xlabel("Number of Heads $k$ [dimensionless]", fontsize=10)
    ax.set_ylabel("Probability $P(k)$ [dimensionless]", fontsize=10)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", frameon=True)

    plt.tight_layout()
    plt.savefig(path, format="pdf" if path.suffix == ".pdf" else None)
    plt.close(fig)


def figure_probabilities(N: int, k0: int, path: Path) -> None:
    """Item 2: P_k for the team's N with the +-10 / +-20 windows marked."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

    k = np.arange(N + 1)
    p_exact = prob_array(N)

    # Plot discrete probability distribution
    ax.plot(k, p_exact, color="#2b5c8f", linewidth=1.5, label=f"$P(k)$ for $N = {N}$")

    # Mark central peak k0 = N // 2
    p_peak = prob(N, k0)
    ax.axvline(k0, color="black", linestyle="--", linewidth=1.2, label=f"Peak $k_0 = {k0}$ ($P={p_peak:.4f}$)")

    # Highlight +-10 and +-20 windows around peak
    if k0 - 10 >= 0 and k0 + 10 <= N:
        ax.axvspan(k0 - 10, k0 + 10, color="#2b5c8f", alpha=0.2, label="$k_0 \\pm 10$ Window")
    if k0 - 20 >= 0 and k0 + 20 <= N:
        ax.axvspan(k0 - 20, k0 + 20, color="#d95f02", alpha=0.1, label="$k_0 \\pm 20$ Window")

    ax.set_title(f"Macrostate Probability Distribution ($N = {N}$, Peak $k_0 = {k0}$)", fontsize=12)
    ax.set_xlabel("Number of Heads $k$ [dimensionless]", fontsize=10)
    ax.set_ylabel("Probability $P_k$ [dimensionless]", fontsize=10)
    ax.set_xlim(0, N)
    ax.set_ylim(bottom=0)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", frameon=True)

    plt.tight_layout()
    plt.savefig(path, format="pdf" if path.suffix == ".pdf" else None)
    plt.close(fig)


def figure_timing(path: Path) -> None:
    """Item 1b: wall-clock time versus N for brute-force microstate generation."""
    path.parent.mkdir(parents=True, exist_ok=True)

    # Measure execution time for generating 2^N microstates directly
    Ns = list(range(1, 18))
    times = []

    for n in Ns:
        t0 = time.perf_counter()
        # Brute-force iterate over all 2^n binary microstate integers
        _ = [bin(i) for i in range(1 << n)]
        t1 = time.perf_counter()
        times.append(t1 - t0)

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

    ax.plot(Ns, times, "o-", color="#e7298a", linewidth=2, markersize=5, label="Brute-Force $2^N$ Microstates")

    ax.set_yscale("log")
    ax.set_title("Brute-Force Microstate Generation Timing vs. System Size $N$", fontsize=12)
    ax.set_xlabel("System Size $N$ [coins]", fontsize=10)
    ax.set_ylabel("Wall-Clock Time [seconds]", fontsize=10)
    ax.grid(True, which="both", linestyle=":", alpha=0.6)
    ax.legend(loc="upper left", frameon=True)

    plt.tight_layout()
    plt.savefig(path, format="pdf" if path.suffix == ".pdf" else None)
    plt.close(fig)


def generate_all_figures(digits: list[int], out_dir: Path = Path("report/figures")) -> None:
    """Helper function to generate all vector figures for the report."""
    M = harmonic_mean_M(digits)
    N = 100 + M
    k0 = N // 2

    figure_distributions([10, 30, 50, N], out_dir / "figure_distributions.pdf")
    figure_probabilities(N, k0, out_dir / "figure_probabilities.pdf")
    figure_timing(out_dir / "figure_timing.pdf")
