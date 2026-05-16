"""Command-line entry point for the DSM ambulance-location case studies.

Selects a case (1 = 3 stations, 2 = 4 stations) and lets the user override
rt1 and lamda from the command line so the four headline numbers reported
in the README can be reproduced without editing source.

Examples
--------
    python run.py --case 1                # case 1 with case-1 defaults
    python run.py --case 1 --rt1 10       # case 1 reproduced at rt1 = 10 min
    python run.py --case 2 --rt1 10 --lamda 0.9
"""
from __future__ import annotations

import argparse
import sys

import case1
import case2
from dsm import format_report, solve_dsm


CASES = {
    1: {
        "module": case1,
        "default_rt1": 8,
        "default_lamda": 0.42,
    },
    2: {
        "module": case2,
        "default_rt1": 8,
        "default_lamda": 0.6,
    },
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Solve the DSM ambulance-location model for the Patras case study.",
    )
    parser.add_argument(
        "--case",
        type=int,
        choices=(1, 2),
        required=True,
        help="1 = 3 existing stations, 2 = 4 stations including Pampeloponnisiako.",
    )
    parser.add_argument(
        "--rt1",
        type=int,
        default=None,
        help="Primary response-time threshold in minutes (default: case-specific).",
    )
    parser.add_argument(
        "--lamda",
        type=float,
        default=None,
        help="Minimum single-coverage fraction within rt1 (default: case-specific).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show pymprog solver progress.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    case = CASES[args.case]
    module = case["module"]
    rt1 = args.rt1 if args.rt1 is not None else case["default_rt1"]
    lamda = args.lamda if args.lamda is not None else case["default_lamda"]

    result = solve_dsm(
        module.TIME,
        module.DEMAND,
        P=module.P,
        rt1=rt1,
        lamda=lamda,
        verbose=args.verbose,
    )
    print(format_report(result, rt1=rt1, lamda=lamda, station_names=module.STATION_NAMES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
