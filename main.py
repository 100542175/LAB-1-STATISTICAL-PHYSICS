#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Import modular packages from src/
from src import combinatorics, microstates, thermodynamics


def part1a(ctx):
    """Part 1a: Microstate table for N = 7 coins."""
    microstates.print_n7_table()


def part1b(ctx):
    """Part 1b: Exact multiplicity & probability generation."""
    digits = ctx.get("digits", [14, 75, 92, 99])
    M = combinatorics.harmonic_mean_M(digits)
    N = 100 + M
    print(f"[Part 1b] Harmonic Mean M = {M}, N = {N}")


def part1c(ctx):
    """Part 1c: Float overflow limit check."""
    max_n = combinatorics.largest_N_with_float_omega()
    print(f"[Part 1c] Largest N fitting in double float: N = {max_n}")


def part1d(ctx):
    pass


def part1e(ctx):
    pass


def part2_prob(ctx):
    """Items 2a-2d: Probability calculations for N = 100 + M."""
    digits = ctx.get("digits", [14, 75, 92, 99])
    combinatorics.print_probability_report(digits)


def part2_entropy(ctx):
    """Items 2e-2k: Thermodynamics, entropy, waiting times, and Large-N limit."""
    digits = ctx.get("digits", [14, 75, 92, 99])
    thermodynamics.print_thermodynamics_report(digits)


def part2_implications(ctx):
    """Items 2h-2j: Handled inside print_thermodynamics_report."""
    pass


def part2_large_n(ctx):
    """Item 2k: Handled inside print_thermodynamics_report."""
    pass


SECTIONS = [
    part1a,
    part1b,
    part1c,
    part2_prob,
    part2_entropy,
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
    ap.add_argument("--out", type=Path, default=Path("report"))
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
