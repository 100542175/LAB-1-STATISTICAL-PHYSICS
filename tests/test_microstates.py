"""Unit tests for src/microstates.py."""
import math

import pytest

from src.microstates import (
    iter_microstates,
    to_string,
    count_heads,
    macrostate_counts,
    microstates_by_macrostate,
    benchmark,
    peak_memory_bytes,
    measure_enumeration,
    extrapolate_max_N,
    n7_table_rows,
    n7_listing_lines,
)


def test_generator_yields_2_pow_N_distinct_states():
    for N in [0, 1, 5, 10]:
        states = list(iter_microstates(N))
        assert len(states) == 2 ** N
        assert len(set(states)) == 2 ** N
        assert min(states) == 0
        assert max(states) == 2 ** N - 1


def test_generator_rejects_negative_N():
    with pytest.raises(ValueError):
        list(iter_microstates(-1))


def test_counts_are_binomial():
    for N in [1, 2, 6, 7, 12, 16]:
        counts = macrostate_counts(N)
        assert counts == [math.comb(N, k) for k in range(N + 1)]
        assert sum(counts) == 2 ** N


def test_manual_table_1_for_N5():
    grouped = microstates_by_macrostate(5)
    assert len(grouped) == 6
    assert grouped[5] == ["HHHHH"]
    assert grouped[0] == ["TTTTT"]
    # rows k = 4 and k = 1 of Table 1 of the manual (order-independent)
    assert sorted(grouped[4]) == sorted(["HHHHT", "HHHTH", "HHTHH", "HTHHH", "THHHH"])
    assert sorted(grouped[1]) == sorted(["TTTTH", "TTTHT", "TTHTT", "THTTT", "HTTTT"])
    # rows k = 3 and k = 2
    assert sorted(grouped[3]) == sorted(["HTHTH", "THTHH", "HTHHT", "THHTH", "THHHT",
                                         "HHTTH", "HHTHT", "HHHTT", "HTTHH", "TTHHH"])
    for k in range(6):
        assert len(grouped[k]) == math.comb(5, k)
        assert all(s.count("H") == k and len(s) == 5 for s in grouped[k])


def test_to_string_and_count_heads():
    s = 0b10110                      # 22, N = 5
    assert to_string(s, 5) == "HTHHT"
    assert count_heads(s) == 3
    assert to_string(0, 4) == "TTTT"
    assert to_string(15, 4) == "HHHH"
    assert count_heads(0) == 0


def test_to_string_edge_cases_and_errors():
    assert to_string(0, 0) == ""                 # N = 0: empty string, not 'T'
    assert to_string(1, 1) == "H"
    with pytest.raises(ValueError):
        to_string(1, 0)
    with pytest.raises(ValueError):
        to_string(16, 4)                         # out of range
    with pytest.raises(ValueError):
        to_string(-1, 4)
    with pytest.raises(ValueError):
        to_string(0, -1)
    with pytest.raises(ValueError):
        count_heads(-3)


def test_to_string_roundtrip_with_count_heads():
    for s in range(64):
        assert to_string(s, 6).count("H") == count_heads(s)


def test_benchmark_and_peak_memory():
    def dummy_run(N: int):
        _ = [s for s in iter_microstates(N)]

    mean_t, std_t = benchmark(dummy_run, N=8, repeats=3)
    assert mean_t > 0
    assert std_t >= 0
    assert benchmark(dummy_run, N=8, repeats=1)[1] == 0.0
    with pytest.raises(ValueError):
        benchmark(dummy_run, N=8, repeats=0)

    assert peak_memory_bytes(dummy_run, N=8) > 0


def test_generator_uses_far_less_memory_than_a_list():
    def as_list(N):
        return list(iter_microstates(N))

    def count_only(N):
        macrostate_counts(N)

    assert peak_memory_bytes(count_only, 14) < peak_memory_bytes(as_list, 14) / 10


def test_measure_enumeration_structure_and_growth():
    data = measure_enumeration([8, 10, 12], repeats=2)
    assert [d[0] for d in data] == [8, 10, 12]
    assert all(d[1] > 0 and d[2] >= 0 for d in data)
    assert data[2][1] > data[0][1]             # more microstates -> more time


def test_extrapolate_max_N():
    assert extrapolate_max_N(30, 150.0) == 31          # one doubling left
    assert extrapolate_max_N(30, 300.0) == 30
    assert extrapolate_max_N(30, 40.0) == 32           # 40 -> 80 -> 160 (still fits) -> 320
    assert extrapolate_max_N(30, 600.0) == 29          # already too slow: go down
    with pytest.raises(ValueError):
        extrapolate_max_N(30, 0.0)


def test_n7_table_rows():
    rows = n7_table_rows(7)
    assert [r[0] for r in rows] == [7, 6, 5, 4, 3, 2, 1, 0]
    assert [r[1] for r in rows] == [1, 7, 21, 35, 35, 21, 7, 1]
    assert sum(r[1] for r in rows) == 128
    assert pytest.approx(sum(r[2] for r in rows), abs=1e-12) == 1.0


def test_n7_listing_contains_all_128_microstates():
    lines = n7_listing_lines(7)
    assert len(lines) == 8
    strings = [s for line in lines for s in line.split(": ")[1].split(", ")]
    assert len(strings) == 128
    assert len(set(strings)) == 128
