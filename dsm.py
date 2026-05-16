"""Double Standard Model (DSM) solver for ambulance location.

Implements the integer-programming formulation from Gendreau (1997). Given
travel times between stations and points of interest, a demand vector, and
two coverage thresholds (rt1 and rt2), the solver places ambulances so as
to maximize weighted double-coverage within rt1 while guaranteeing single
coverage within rt2 and a minimum coverage fraction within rt1.
"""
from __future__ import annotations

from typing import NamedTuple, Sequence

import numpy as np
from pymprog import model


class DSMResult(NamedTuple):
    """Solution of the DSM integer program."""

    objective: float
    rt2: int
    ambulances_per_station: list[int]
    total_demand: float

    @property
    def double_coverage_ratio(self) -> float:
        return self.objective / self.total_demand


def derive_rt2(time: np.ndarray) -> int:
    """Worst best-case travel time: max over points of (min over stations).

    Using this as rt2 guarantees every point can be reached by at least one
    station within rt2, which is the minimum feasibility requirement of the
    DSM single-coverage constraint.
    """
    return int(np.asarray(time).min(axis=0).max())


def solve_dsm(
    time: np.ndarray,
    demand: np.ndarray,
    P: int,
    rt1: int,
    lamda: float,
    rt2: int | None = None,
    verbose: bool = False,
) -> DSMResult:
    """Solve the Double Standard Model.

    Parameters
    ----------
    time : array of shape (S, N), travel times in minutes from each of S
        stations (rows) to each of N points of interest (columns).
    demand : array of shape (N,), emergency-call weights per point of
        interest.
    P : upper bound on the total number of ambulances.
    rt1 : primary response-time threshold in minutes. Points reached within
        rt1 contribute to the double-coverage objective.
    lamda : minimum fraction of weighted demand that must be reached at
        least once within rt1.
    rt2 : secondary threshold in minutes. Defaults to ``derive_rt2(time)``.
    verbose : pass-through to pymprog's solver verbosity.
    """
    time = np.asarray(time)
    demand = np.asarray(demand)
    n_stations, n_points = time.shape
    if demand.shape != (n_points,):
        raise ValueError(
            f"demand has shape {demand.shape}, expected ({n_points},)"
        )

    if rt2 is None:
        rt2 = derive_rt2(time)

    a = (time <= rt1).astype(int)
    b = (time <= rt2).astype(int)
    Pj = P - n_stations  # per-station cap, matching the original scripts
    total_demand = float(demand.sum())

    p = model("Ambulance DSM")
    p.verbose(verbose)

    x1 = p.var("x1", n_points, kind=int, bounds=(0, 1))
    x2 = p.var("x2", n_points, kind=int, bounds=(0, 1))
    y = p.var("y", n_stations, kind=int, bounds=(1, Pj))

    p.maximize(sum(demand[i] * x2[i] for i in range(n_points)))

    # pymprog registers each `>=` expression with the active model on
    # construction; the resulting value is discarded but the constraint is
    # already attached. Hence the dangling expressions below are intentional.

    for j in range(n_points):                                            # R1
        sum(y[i] * b[i][j] for i in range(n_stations)) >= 1

    sum(demand[i] * x1[i] for i in range(n_points)) >= lamda * total_demand  # R2

    for j in range(n_points):                                            # R3
        sum(y[i] * a[i][j] for i in range(n_stations)) - x1[j] - x2[j] >= 0

    for i in range(n_points):                                            # R4
        x1[i] >= x2[i]

    sum(y[i] for i in range(n_stations)) <= P                            # R5

    p.solve()

    objective = sum(demand[i] * x2[i].primal for i in range(n_points))
    counts = [int(round(y[i].primal)) for i in range(n_stations)]

    p.end()

    return DSMResult(
        objective=float(objective),
        rt2=int(rt2),
        ambulances_per_station=counts,
        total_demand=total_demand,
    )


def format_report(
    result: DSMResult,
    rt1: int,
    lamda: float,
    station_names: Sequence[str] | None = None,
) -> str:
    """Render a DSM result as a human-readable block of text."""
    names = station_names or [
        f"station {i + 1}" for i in range(len(result.ambulances_per_station))
    ]
    lines = [
        f"Single-coverage floor: {lamda * 100:.1f}% within rt1 = {rt1} min",
        f"Maximum response time (rt2): {result.rt2} min",
        f"Objective (weighted double coverage): "
        f"{result.objective:.1f} / {result.total_demand:.1f} "
        f"({result.double_coverage_ratio * 100:.1f}%)",
        "Ambulances per station:",
    ]
    for name, count in zip(names, result.ambulances_per_station):
        lines.append(f"  {name}: {count}")
    return "\n".join(lines)
