#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src import combinatorics, microstates, thermodynamics, plots


def part1a(ctx):
    microstates.print_n7_table()


def part1b(ctx):
    digits = ctx.get("digits", [14, 75, 92, 99])
    M = combinatorics.harmonic_mean_M(digits)
    N = 100 + M
    print(f"[Part 1b] Harmonic Mean M = {M}, N = {N}")


def part1c(ctx):
    max_n = combinatorics.largest_N_with_float_omega()
    print(f"[Part 1c] Largest N fitting in double float: N = {max_n}")


def part2_prob(ctx):
    digits = ctx.get("digits", [14, 75, 92, 99])
    combinatorics.print_probability_report(digits)


def part2_entropy(ctx):
    digits = ctx.get("digits", [14, 75, 92, 99])
    thermodynamics.print_thermodynamics_report(digits)


def part3_plots(ctx):
    digits = ctx.get("digits", [14, 75, 92, 99])
    out_dir = ctx.get("out", Path("report/figures"))
    plots.generate_all_figures(digits, out_dir)


SECTIONS = [
    part1a,
    part1b,
    part1c,
    part2_prob,
    part2_entropy,
    part3_plots,
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Statistical Physics Lab 1 Runner")
    ap.add_argument(
        "--digits",
        type=int,
        nargs="+",
        default=[14, 75, 92, 99],
        help="last two digits of each team member's NIA",
    )
    ap.add_argument("--out", type=Path, default=Path("report/figures"))
    args = ap.parse_args()
    ctx = {"digits": args.digits, "out": args.out}

    for section in SECTIONS:
        try:
            section(ctx)
            print(f"[done] {section.__name__}\n")
        except NotImplementedError:
            print(f"[TODO] {section.__name__}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
