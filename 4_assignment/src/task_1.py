"""Problem 1: unbounded LP analysis."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from assignment_data import PROBLEM_1
from lp_utils import feasible_vertices_2d, plot_2d_problem, solve_maximization


def analyze_problem_1() -> dict[str, object]:
    result = solve_maximization(
        objective=PROBLEM_1["objective"],
        a_ub=PROBLEM_1["A_ub"],
        b_ub=PROBLEM_1["b_ub"],
        bounds=PROBLEM_1["bounds"],
    )
    vertices = feasible_vertices_2d(
        a_ub=PROBLEM_1["A_ub"],
        b_ub=PROBLEM_1["b_ub"],
        bounds=PROBLEM_1["bounds"],
    )
    ray_start = (1.0, 2.0)
    ray_direction = (1.0, 1.0)
    sample_points = tuple((value, value + 1.0) for value in (1.0, 2.0, 3.0, 5.0))
    sample_objectives = tuple(2.0 * x_value + 3.0 * y_value for x_value, y_value in sample_points)
    return {
        "status": result.status,
        "message": result.message,
        "is_unbounded": result.status == 3,
        "vertices": vertices,
        "ray_start": ray_start,
        "ray_direction": ray_direction,
        "sample_points": sample_points,
        "sample_objectives": sample_objectives,
    }


def render_problem_1_plot(path: str | Path) -> Path:
    return plot_2d_problem(
        path=path,
        title="Problem 1: Unbounded feasible region",
        line_functions=[
            ("3x1 + x2 = 3", lambda x_value: 3.0 - 3.0 * x_value),
            ("x2 = x1 + 1", lambda x_value: x_value + 1.0),
            ("x2 = 3x1 + 1.5", lambda x_value: 3.0 * x_value + 1.5),
        ],
        feasible_mask=lambda x_value, y_value: (
            (3.0 * x_value + y_value >= 3.0)
            & (y_value >= x_value + 1.0)
            & (-6.0 * x_value + 2.0 * y_value <= 3.0)
            & (x_value >= 0.0)
            & (y_value >= 0.0)
        ),
        x_range=(0.0, 4.5),
        y_range=(0.0, 8.0),
        vertices=analyze_problem_1()["vertices"],
        annotation="Feasible ray: x2 = x1 + 1 for x1 >= 1",
    )

