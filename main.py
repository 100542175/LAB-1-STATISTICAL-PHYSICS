#!/usr/bin/env python3
"""Run the whole Lab 1 analysis.  Each section prints TODO until it is implemented.

Usage:  python main.py [--digits D1 D2 ...] [--out report]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# from src import combinatorics, microstates, thermodynamics, plots   # TODO: use them below


def part1a(ctx):  # N = 7: list microstates by macrostate
    raise NotImplementedError


def part1b(ctx):  # largest N with full enumeration, time and RAM
    raise NotImplementedError


def part1c(ctx):  # Omega(N, k), N = 20, 50, 80, 100, one figure
    raise NotImplementedError


def part1d(ctx):  # largest N for the distribution
    raise NotImplementedError


def part1e(ctx):  # thermodynamic limit
    raise NotImplementedError


def part2_prob(ctx):  # items a)-d)
    raise NotImplementedError


def part2_entropy(ctx):  # items e)-g)
    raise NotImplementedError


def part2_implications(ctx):  # items h)-j)
    raise NotImplementedError


def part2_large_n(ctx):  # item k)
    raise NotImplementedError


SECTIONS = [part1a, part1b, part1c, part1d, part1e,
            part2_prob, part2_entropy, part2_implications, part2_large_n]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--digits", type=int, nargs="+", default=[0],
                    help="last two digits of each team member's NIA")
    ap.add_argument("--out", type=Path, default=Path("report"))
    args = ap.parse_args()
    ctx = {"digits": args.digits, "out": args.out}   # TODO: add M, N = 100 + M here
    for section in SECTIONS:
        try:
            section(ctx)
            print(f"[done] {section.__name__}")
        except NotImplementedError:
            print(f"[TODO] {section.__name__}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
