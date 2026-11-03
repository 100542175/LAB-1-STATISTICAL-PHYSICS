#!/usr/bin/env python3
"""Statistical Physics Lab 1 runner: executes every item of the manual in order.

Usage (from the project root, environment active):
    python main.py                       # default run (about a minute)
    python main.py --quick               # a few seconds, for testing
    python main.py --digits 23 47 61 85  # your team's NIA digits (last two digits each)
    python main.py --max-bench 26        # larger enumeration benchmark (slower)
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

from src import combinatorics, microstates, plots, thermodynamics

DEFAULT_DIGITS = [14, 75, 92, 99]          # EXAMPLE values: replace with your team's NIAs


def team_N(ctx: dict) -> int:
    """N = 100 + M for the team's NIA digits (must be below 200)."""
    M = combinatorics.harmonic_mean_M(ctx["digits"])
    N = 100 + M
    if N >= 200:
        raise ValueError(f"N = {N} must be below 200; check the NIA digits.")
    ctx["results"].update(M=M, N=N)
    return N


# ------------------------------------------------------------------ Part 1
def part1a(ctx: dict) -> None:
    """1a: enumeration for N = 7 (multiplicities + every microstate)."""
    microstates.print_n7_table(show_microstates=True)


def part1b(ctx: dict) -> None:
    """1b: largest N with full enumeration: time (mean +- std), memory, extrapolation."""
    Ns = ctx["bench_Ns"]
    print("[1b] Timing the full enumeration (generator + bit_count):")
    data = []
    for n in Ns:
        reps = ctx["repeats"] if n <= 24 else 1
        mean, std = microstates.benchmark(microstates.macrostate_counts, n, reps)
        data.append((n, mean, std))
        print(f"     N = {n:2d}   2^N = {2 ** n:>12,d}   t = {mean:9.4f} +- {std:.4f} s   ({reps} runs)")
    mem_gen = microstates.peak_memory_bytes(microstates.macrostate_counts, 14)
    mem_list = microstates.peak_memory_bytes(lambda n: list(microstates.iter_microstates(n)), 14)
    n_last, t_last, _ = data[-1]
    n_max = microstates.extrapolate_max_N(n_last, t_last, plots.BUDGET_S)
    print(f"[1b] Peak memory at N = 14: generator {mem_gen / 1e3:.1f} kB vs storing all states {mem_list / 1e6:.2f} MB")
    print(f"[1b] Extrapolated largest N in 5 minutes: N = {n_max} "
          f"(time doubles per +1 in N; last measurement N = {n_last}, {t_last:.3g} s)")
    print(f"[1b] Storing 2^N states of N bits would need {n_max * 2 ** n_max / 8 / 1e9:.1f} GB at N = {n_max}.")
    plots.figure_timing(data, ctx["out"] / "figure_timing.pdf", plots.BUDGET_S)
    ctx["results"].update(bench=data, N_max_extrapolated=n_max,
                          mem_generator_B=mem_gen, mem_list_N14_B=mem_list)


def part1c(ctx: dict) -> None:
    """1c: Omega(N,k) for N = 20, 50, 80, 100 and one figure."""
    print("[1c] Macrostate distributions:")
    print(f"     {'N':>4} {'2^N':>12} {'Omega(N,N/2)':>14} {'P_(N/2)':>10} {'sigma':>7} {'sigma/mu':>9}")
    for n in plots.DISTRIBUTION_NS:
        probs = combinatorics.prob_array(n)
        assert abs(probs.sum() - 1.0) < 1e-12
        print(f"     {n:>4} {2.0 ** n:>12.3e} {float(math.comb(n, n // 2)):>14.4e} "
              f"{probs.max():>10.4f} {thermodynamics.sigma(n):>7.2f} {thermodynamics.relative_width(n):>9.3f}")
    plots.figure_distributions(plots.DISTRIBUTION_NS, ctx["out"] / "figure_distributions.pdf")


def part1d(ctx: dict) -> None:
    """1d: largest N for the distribution (overflow limit and log-space scaling)."""
    n_float = combinatorics.largest_N_with_float_omega()
    print(f"[1d] Omega(N, N/2) fits in a double only up to N = {n_float} (overflow above ~1.8e308).")
    print("[1d] Log-space distribution for large N (vectorised gammaln):")
    print(f"     {'N':>9} {'time (s)':>10} {'array (MB)':>11} {'|sum P_k - 1|':>15}")
    rows = []
    for exp in range(3, ctx["dist_max_exp"] + 1):
        n = 10 ** exp
        t0 = time.perf_counter()
        probs = combinatorics.prob_array(n)
        dt = time.perf_counter() - t0
        dev = abs(float(probs.sum()) - 1.0)
        print(f"     {n:>9,d} {dt:>10.3f} {probs.nbytes / 1e6:>11.1f} {dev:>15.2e}")
        rows.append((n, dt, dev))
    ctx["results"].update(N_float_overflow=n_float, dist_scaling=rows)


def part1e(ctx: dict) -> None:
    """1e: thermodynamic limit (Gaussian, relative width 1/sqrt(N))."""
    print("[1e] Relative width sigma/mu = 1/sqrt(N):")
    for n in (100, 10 ** 4, 10 ** 8, 10 ** 23):
        print(f"     N = {n:>10.1e}   sigma = {thermodynamics.sigma(n):>10.3e} heads   "
              f"sigma/mu = {thermodynamics.relative_width(n):.3e}")


# ------------------------------------------------------------------ Part 2
def part2_prob(ctx: dict) -> None:
    """2a-d: probabilities for the team's N, and the figure."""
    N = team_N(ctx)
    combinatorics.print_probability_report(ctx["digits"])
    plots.figure_probabilities(N, N // 2, ctx["out"] / "figure_probabilities.pdf")


def part2_thermo(ctx: dict) -> None:
    """2e-k: entropy, waiting time, likelihood ratios, N -> 1e23."""
    team_N(ctx)
    thermodynamics.print_thermodynamics_report(ctx["digits"])


SECTIONS = [part1a, part1b, part1c, part1d, part1e, part2_prob, part2_thermo]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Statistical Physics Lab 1 Runner")
    ap.add_argument("--digits", type=int, nargs="+", default=DEFAULT_DIGITS,
                    help="last two digits of each team member's NIA")
    ap.add_argument("--out", type=Path, default=Path("report/figures"))
    ap.add_argument("--max-bench", type=int, default=22,
                    help="largest N of the enumeration benchmark (time doubles per +1)")
    ap.add_argument("--dist-max-exp", type=int, default=6,
                    help="largest N = 10**exp tried for the log-space distribution")
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--quick", action="store_true", help="small benchmarks (seconds)")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.quick:
        args.max_bench, args.dist_max_exp, args.repeats = 18, 4, 2
    ctx = {
        "digits": args.digits,
        "out": args.out,
        "bench_Ns": list(range(12, args.max_bench + 1, 2)),
        "dist_max_exp": args.dist_max_exp,
        "repeats": args.repeats,
        "results": {"digits": args.digits},
    }
    ctx["out"].mkdir(parents=True, exist_ok=True)

    for section in SECTIONS:
        try:
            section(ctx)
            print(f"[done] {section.__name__}\n")
        except NotImplementedError:
            print(f"[TODO] {section.__name__}\n")

    results_path = ctx["out"].parent / "results.json"
    results_path.write_text(json.dumps(ctx["results"], indent=2, default=str))
    print(f"Figures in {ctx['out']}; raw numbers in {results_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())