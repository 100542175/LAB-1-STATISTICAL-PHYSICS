"""Vector (PDF) figures for the report.  (TEAM TO IMPLEMENT)

Every axis needs a label with units ('dimensionless' counts), and the caption goes in LaTeX.
"""
from __future__ import annotations

from pathlib import Path


def figure_distributions(Ns: list[int], path: Path) -> None:
    """Item 1c: macrostate distribution versus k for all N in one figure."""
    raise NotImplementedError


def figure_probabilities(N: int, k0: int, path: Path) -> None:
    """Item 2: P_k for the team's N with the +-10 / +-20 windows marked."""
    raise NotImplementedError


def figure_timing(path: Path) -> None:
    """Item 1b: wall-clock time versus N."""
    raise NotImplementedError
