"""Unit tests for src/plots.py."""
from pathlib import Path
import pytest
from src.plots import figure_distributions, figure_probabilities, figure_timing, generate_all_figures


def test_figure_distributions_creates_pdf(tmp_path: Path):
    out_pdf = tmp_path / "distributions.pdf"
    figure_distributions([10, 20, 30], out_pdf)
    assert out_pdf.exists()
    assert out_pdf.stat().st_size > 0


def test_figure_probabilities_creates_pdf(tmp_path: Path):
    out_pdf = tmp_path / "probabilities.pdf"
    figure_probabilities(138, 69, out_pdf)
    assert out_pdf.exists()
    assert out_pdf.stat().st_size > 0


def test_figure_timing_creates_pdf(tmp_path: Path):
    out_pdf = tmp_path / "timing.pdf"
    figure_timing(out_pdf)
    assert out_pdf.exists()
    assert out_pdf.stat().st_size > 0


def test_generate_all_figures(tmp_path: Path):
    generate_all_figures([14, 75, 92, 99], tmp_path)
    assert (tmp_path / "figure_distributions.pdf").exists()
    assert (tmp_path / "figure_probabilities.pdf").exists()
    assert (tmp_path / "figure_timing.pdf").exists()