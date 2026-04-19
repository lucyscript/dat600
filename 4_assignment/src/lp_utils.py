"""Shared helpers for LP analysis and local plotting."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog


matplotlib.use("Agg")


@dataclass(frozen=True)
class LPResult:
    success: bool
    status: int
    message: str
    solution: tuple[float, ...] | None
    objective_value: float | None


def solve_maximization(
    objective: Iterable[float],
    a_ub: Iterable[Iterable[float]],
    b_ub: Iterable[float],
    bounds: Iterable[tuple[float | None, float | None]],
) -> LPResult:
    coefficients = [-value for value in objective]
    result = linprog(c=coefficients, A_ub=list(a_ub), b_ub=list(b_ub), bounds=list(bounds), method="highs")
    objective_value = None if result.fun is None else -float(result.fun)
    solution = None if result.x is None else tuple(float(value) for value in result.x)
    return LPResult(
        success=bool(result.success),
        status=int(result.status),
        message=str(result.message),
        solution=solution,
        objective_value=objective_value,
    )


def solve_feasibility(
    a_ub: Iterable[Iterable[float]],
    b_ub: Iterable[float],
    bounds: Iterable[tuple[float | None, float | None]],
) -> LPResult:
    dimension = len(list(bounds))
    result = linprog(
        c=[0.0] * dimension,
        A_ub=list(a_ub),
        b_ub=list(b_ub),
        bounds=list(bounds),
        method="highs",
    )
    solution = None if result.x is None else tuple(float(value) for value in result.x)
    return LPResult(
        success=bool(result.success),
        status=int(result.status),
        message=str(result.message),
        solution=solution,
        objective_value=0.0 if result.success else None,
    )


def inequality_satisfied(point: tuple[float, float], row: Iterable[float], rhs: float, tolerance: float = 1e-9) -> bool:
    return float(np.dot(np.array(list(row), dtype=float), np.array(point, dtype=float))) <= rhs + tolerance


def feasible_vertices_2d(
    a_ub: Iterable[Iterable[float]],
    b_ub: Iterable[float],
    bounds: Iterable[tuple[float | None, float | None]],
) -> tuple[tuple[float, float], ...]:
    rows = [tuple(row) for row in a_ub]
    rhs_values = list(b_ub)
    boundary_lines: list[tuple[float, float, float]] = [(row[0], row[1], rhs) for row, rhs in zip(rows, rhs_values, strict=True)]
    lower_x = next((bound[0] for index, bound in enumerate(bounds) if index == 0), 0.0) or 0.0
    lower_y = next((bound[0] for index, bound in enumerate(bounds) if index == 1), 0.0) or 0.0
    boundary_lines.extend([(1.0, 0.0, lower_x), (0.0, 1.0, lower_y)])

    vertices: list[tuple[float, float]] = []
    for left, right in combinations(boundary_lines, 2):
        point = intersect_lines(left, right)
        if point is None:
            continue
        if point[0] < lower_x - 1e-9 or point[1] < lower_y - 1e-9:
            continue
        if all(inequality_satisfied(point, row, rhs) for row, rhs in zip(rows, rhs_values, strict=True)):
            rounded = tuple(0.0 if abs(value) < 1e-10 else round(value, 10) for value in point)
            if rounded not in vertices:
                vertices.append(rounded)
    return tuple(sorted(vertices))


def intersect_lines(
    left: tuple[float, float, float],
    right: tuple[float, float, float],
) -> tuple[float, float] | None:
    a1, b1, c1 = left
    a2, b2, c2 = right
    determinant = a1 * b2 - a2 * b1
    if abs(determinant) < 1e-12:
        return None
    x_value = (c1 * b2 - c2 * b1) / determinant
    y_value = (a1 * c2 - a2 * c1) / determinant
    return x_value, y_value


def plot_2d_problem(
    path: str | Path,
    title: str,
    line_functions: list[tuple[str, callable]],
    feasible_mask: callable,
    x_range: tuple[float, float],
    y_range: tuple[float, float],
    vertices: Iterable[tuple[float, float]] = (),
    annotation: str | None = None,
) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    x_values = np.linspace(x_range[0], x_range[1], 800)
    grid_x, grid_y = np.meshgrid(np.linspace(x_range[0], x_range[1], 500), np.linspace(y_range[0], y_range[1], 500))
    mask = feasible_mask(grid_x, grid_y)

    plt.figure(figsize=(7.5, 5.5))
    plt.contourf(grid_x, grid_y, mask.astype(int), levels=[0.5, 1.5], colors=["#d6f5d6"], alpha=0.6)
    for label, function in line_functions:
        plt.plot(x_values, function(x_values), label=label, linewidth=2)

    if vertices:
        xs, ys = zip(*vertices, strict=True)
        plt.scatter(xs, ys, color="black", zorder=3)
        for x_value, y_value in vertices:
            plt.annotate(f"({x_value:.3g}, {y_value:.3g})", (x_value, y_value), textcoords="offset points", xytext=(5, 5))

    if annotation:
        plt.text(0.02, 0.02, annotation, transform=plt.gca().transAxes, fontsize=9, bbox={"facecolor": "white", "alpha": 0.8})

    plt.xlim(*x_range)
    plt.ylim(*y_range)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title(title)
    plt.legend(loc="best")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()
    return output_path
