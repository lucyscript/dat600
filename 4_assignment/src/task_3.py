"""Problem 3: LP solution used to verify the MATLAB result."""

from __future__ import annotations

from assignment_data import PROBLEM_3
from lp_utils import solve_maximization


def analyze_problem_3() -> dict[str, object]:
    optimum = solve_maximization(
        objective=PROBLEM_3["objective"],
        a_ub=PROBLEM_3["A_ub"],
        b_ub=PROBLEM_3["b_ub"],
        bounds=PROBLEM_3["bounds"],
    )
    return {
        "solution": None if optimum.solution is None else tuple(round(value, 10) for value in optimum.solution),
        "max_value": None if optimum.objective_value is None else round(optimum.objective_value, 10),
        "message": optimum.message,
    }

