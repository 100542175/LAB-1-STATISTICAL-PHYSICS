"""Unit tests for src/plots.py (smoke tests: files are valid, non-empty PDFs)."""
from pathlib import Path

import pytest

from src.plots import (
    DISTRIBUTION_NS,
    figure_distributions,
    figure_probabilities,
    figure_timing,
    generate_all_figures,
)

FAKE_TIMING = [(10, 0.001, 0.0001), (12, 0.004, 0.0002), (14, 0.016, 0.001),
               (16, 0.064, 0.003), (18, 0.26, 0.01)]


def _is_pdf(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 1000 and path.read_bytes()[:4] == b"%PDF"


def test_distribution_sizes_are_those_of_item_1c():
    assert DISTRIBUTION_NS == [20, 50, 80, 100]


def test_figure_distributions_creates_pdf(tmp_path: Path):
    out_pdf = tmp_path / "sub" / "distributions.pdf"     # also creates the folder
    figure_distributions(DISTRIBUTION_NS, out_pdf)
    assert _is_pdf(out_pdf)


def test_figure_probabilities_creates_pdf(tmp_path: Path):
    out_pdf = tmp_path / "probabilities.pdf"
    figure_probabilities(138, 69, out_pdf)
    assert _is_pdf(out_pdf)


def test_figure_probabilities_small_N_without_windows(tmp_path: Path):
    out_pdf = tmp_path / "small.pdf"
    figure_probabilities(20, 10, out_pdf)                # +-20 window does not fit: no crash
    assert _is_pdf(out_pdf)


def test_figure_timing_uses_given_data_and_returns_Nmax(tmp_path: Path):
    out_pdf = tmp_path / "timing.pdf"
    n_max = figure_timing(FAKE_TIMING, out_pdf)
    assert _is_pdf(out_pdf)
    assert n_max == 18 + 10            # 0.26 s * 2**10 = 266 s <= 300 s < 0.26 * 2**11


def test_figure_timing_needs_two_points(tmp_path: Path):
    with pytest.raises(ValueError):
        figure_timing([(10, 0.001, 0.0)], tmp_path / "t.pdf")


def test_generate_all_figures(tmp_path: Path):
    n_max = generate_all_figures([14, 75, 92, 99], tmp_path, timing_data=FAKE_TIMING)
    assert n_max == 28
    for name in ["figure_distributions.pdf", "figure_probabilities.pdf", "figure_timing.pdf"]:
        assert _is_pdf(tmp_path / name)