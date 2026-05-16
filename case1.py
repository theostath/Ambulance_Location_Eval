"""Case 1: existing layout with 3 ambulance stations in Patras.

10 ambulances distributed across Hospital "Agios Andreas", the University
Hospital, and the Port station. Defaults match the values reported in the
README at rt1 = 8 minutes.
"""
from __future__ import annotations

import numpy as np

from dsm import format_report, solve_dsm


STATION_NAMES = [
    "Hospital 'Agios Andreas'",
    "University Hospital",
    "Port station",
]

# Travel times (minutes) from each station (rows) to each of 12 points of
# interest (columns). Columns: Patra 1-4, Messatida 5-7, Rio 8-9,
# Vraxnaiika 10-11, Paralia 12.
TIME = np.array([
    [10,  7,  9,  5, 10, 10, 11, 14, 18, 15, 18, 11],
    [11, 20, 18, 17, 22, 20, 19,  6, 11, 24, 25, 21],
    [10, 10, 16,  3, 13, 13, 16, 14, 18, 14, 23, 11],
])

# Emergency-call weights per point of interest (sums to 125).
DEMAND = np.array([25, 25, 25, 25, 4, 4, 3, 3, 2, 6, 2, 1])

P = 10  # total ambulance budget


def main(rt1: int = 8, lamda: float = 0.42, verbose: bool = False) -> None:
    result = solve_dsm(TIME, DEMAND, P=P, rt1=rt1, lamda=lamda, verbose=verbose)
    print(format_report(result, rt1=rt1, lamda=lamda, station_names=STATION_NAMES))


if __name__ == "__main__":
    main()
