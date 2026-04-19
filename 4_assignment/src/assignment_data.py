"""Problem data copied from the assignment PDF."""

from __future__ import annotations


PROBLEM_1 = {
    "objective": (2.0, 3.0),
    "maximize": True,
    "A_ub": [
        [-3.0, -1.0],
        [1.0, -1.0],
        [-6.0, 2.0],
    ],
    "b_ub": [-3.0, -1.0, 3.0],
    "bounds": [(0.0, None), (0.0, None)],
}

PROBLEM_2 = {
    "objective": (12.0, -23.0),
    "maximize": True,
    "A_ub": [
        [6.0, -12.0],
        [0.0, 1.0],
        [3.0, -5.0],
    ],
    "b_ub": [-5.0, 1.0, 4.0],
    "bounds": [(0.0, None), (0.0, None)],
    "assignment_claim": "infeasible",
}

PROBLEM_3 = {
    "objective": (3.0, 6.0, 5.0),
    "maximize": True,
    "A_ub": [
        [0.0, 1.0, 2.0],
        [3.0, 2.0, 1.0],
        [1.0, 1.0, 1.0],
    ],
    "b_ub": [6.0, 24.0, 12.0],
    "bounds": [(0.0, None), (0.0, None), (0.0, None)],
}

