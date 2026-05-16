"""Smoke tests pinning the four headline numbers from the README.

These exercise the full pymprog solve path and catch regressions in either
the model formulation or the underlying GLPK behaviour.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure the repo root is importable when pytest runs from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import case1
import case2
from dsm import derive_rt2, solve_dsm


@pytest.mark.parametrize(
    "module, rt1, lamda, expected_objective, expected_rt2",
    [
        (case1, 10, 0.42, 111.0, 18),
        (case1, 8, 0.42, 53.0, 18),
        (case2, 10, 0.6, 114.0, 16),
        (case2, 8, 0.6, 78.0, 16),
    ],
    ids=["case1-rt1=10", "case1-rt1=8", "case2-rt1=10", "case2-rt1=8"],
)
def test_readme_headline_numbers(module, rt1, lamda, expected_objective, expected_rt2):
    result = solve_dsm(module.TIME, module.DEMAND, P=module.P, rt1=rt1, lamda=lamda)
    assert result.objective == expected_objective
    assert result.rt2 == expected_rt2
    assert sum(result.ambulances_per_station) <= module.P


def test_derive_rt2_matches_known_cases():
    assert derive_rt2(case1.TIME) == 18
    assert derive_rt2(case2.TIME) == 16


def test_demand_invariant():
    assert case1.DEMAND.sum() == 125
    assert case2.DEMAND.sum() == 125
