"""Problem 2: feasibility check for the printed constraints."""

from __future__ import annotations

from pathlib import Path

from assignment_data import PROBLEM_2
from lp_utils import feasible_vertices_2d, plot_2d_problem, solve_feasibility, solve_maximization


def analyze_problem_2() -> dict[str, object]:
    feasibility = solve_feasibility(
        a_ub=PROBLEM_2["A_ub"],
        b_ub=PROBLEM_2["b_ub"],
        bounds=PROBLEM_2["bounds"],
    )
    optimum = solve_maximization(
        objective=PROBLEM_2["objective"],
        a_ub=PROBLEM_2["A_ub"],
        b_ub=PROBLEM_2["b_ub"],
        bounds=PROBLEM_2["bounds"],
    )
    vertices = feasible_vertices_2d(
        a_ub=PROBLEM_2["A_ub"],
        b_ub=PROBLEM_2["b_ub"],
        bounds=PROBLEM_2["bounds"],
    )
    return {
        "assignment_claim": PROBLEM_2["assignment_claim"],
        "is_feasible": feasibility.success,
        "feasible_example": None if feasibility.solution is None else tuple(round(value, 10) for value in feasibility.solution),
        "vertices": vertices,
        "claim_matches_constraints": feasibility.success is False,
        "maximizer": None if optimum.solution is None else tuple(round(value, 10) for value in optimum.solution),
        "max_value": None if optimum.objective_value is None else round(optimum.objective_value, 10),
    }


def render_problem_2_plot(path: str | Path) -> Path:
    return plot_2d_problem(
        path=path,
        title="Problem 2: printed constraints are feasible",
        line_functions=[
            ("6x1 - 12x2 = -5", lambda x_value: 0.5 * x_value + 5.0 / 12.0),
            ("x2 = 1", lambda x_value: 0.0 * x_value + 1.0),
            ("3x1 - 5x2 = 4", lambda x_value: 0.6 * x_value - 0.8),
        ],
        feasible_mask=lambda x_value, y_value: (
            (6.0 * x_value - 12.0 * y_value <= -5.0)
            & (y_value <= 1.0)
            & (3.0 * x_value - 5.0 * y_value <= 4.0)
            & (x_value >= 0.0)
            & (y_value >= 0.0)
        ),
        x_range=(0.0, 2.0),
        y_range=(0.0, 1.3),
        vertices=analyze_problem_2()["vertices"],
        annotation="The PDF says infeasible, but the printed region is non-empty.",
    )
