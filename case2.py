"""Case 2: 4 stations after a new station opens at Pampeloponnisiako.

24 ambulances (10 existing + 14 new) distributed across Hospital "Agios
Andreas", the University Hospital, the Port station, and the new
Pampeloponnisiako station. Defaults match the values reported in the README
at rt1 = 8 minutes.
"""
from __future__ import annotations

import numpy as np

from dsm import format_report, solve_dsm


STATION_NAMES = [
    "Hospital 'Agios Andreas'",
    "University Hospital",
    "Port station",
    "Pampeloponnisiako station",
]

TIME = np.array([
    [10,  7,  9,  5, 10, 10, 11, 14, 18, 15, 18, 11],
    [11, 20, 18, 17, 22, 20, 19,  6, 11, 24, 25, 21],
    [10, 10, 16,  3, 13, 13, 16, 14, 18, 14, 23, 11],
    [13,  6,  8,  8,  9,  9,  9, 13, 17, 13, 16, 12],
])

DEMAND = np.array([25, 25, 25, 25, 4, 4, 3, 3, 2, 6, 2, 1])

P = 24  # total ambulance budget (10 existing + 14 new)


def main(rt1: int = 8, lamda: float = 0.6, verbose: bool = False) -> None:
    result = solve_dsm(TIME, DEMAND, P=P, rt1=rt1, lamda=lamda, verbose=verbose)
    print(format_report(result, rt1=rt1, lamda=lamda, station_names=STATION_NAMES))


if __name__ == "__main__":
    main()
