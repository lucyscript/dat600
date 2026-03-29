"""Task 2: cable-network spanning-tree analysis."""

from __future__ import annotations

from algorithms import (
    best_single_weight_swap,
    degree_constrained_kruskal,
    exact_degree_constrained_spanning_tree,
    example_single_weight_swap,
    kruskal_mst,
)
from assignment_data import (
    CABLE_NETWORK_EDGES,
    CABLE_NETWORK_VERTICES,
    DEGREE_LIMIT_COUNTEREXAMPLE_EDGES,
    DEGREE_LIMIT_COUNTEREXAMPLE_LIMITS,
    DEGREE_LIMIT_COUNTEREXAMPLE_VERTICES,
)


def solve_task_2a() -> dict[str, object]:
    mst = kruskal_mst(CABLE_NETWORK_VERTICES, CABLE_NETWORK_EDGES)
    return {
        "mst": mst,
        "within_budget_30": mst.cost <= 30,
    }


def solve_task_2b() -> dict[str, object]:
    degree_limits = {"D": 3}
    exact = exact_degree_constrained_spanning_tree(
        CABLE_NETWORK_VERTICES,
        CABLE_NETWORK_EDGES,
        degree_limits,
    )
    heuristic = degree_constrained_kruskal(
        CABLE_NETWORK_VERTICES,
        CABLE_NETWORK_EDGES,
        degree_limits,
    )
    counterexample_heuristic = degree_constrained_kruskal(
        DEGREE_LIMIT_COUNTEREXAMPLE_VERTICES,
        DEGREE_LIMIT_COUNTEREXAMPLE_EDGES,
        DEGREE_LIMIT_COUNTEREXAMPLE_LIMITS,
    )
    counterexample_optimal = exact_degree_constrained_spanning_tree(
        DEGREE_LIMIT_COUNTEREXAMPLE_VERTICES,
        DEGREE_LIMIT_COUNTEREXAMPLE_EDGES,
        DEGREE_LIMIT_COUNTEREXAMPLE_LIMITS,
    )
    return {
        "exact": exact,
        "heuristic": heuristic,
        "within_budget_30": exact.cost <= 30,
        "counterexample_heuristic": counterexample_heuristic,
        "counterexample_optimal": counterexample_optimal,
    }


def solve_task_2c() -> dict[str, object]:
    example_swap = example_single_weight_swap(
        CABLE_NETWORK_VERTICES,
        CABLE_NETWORK_EDGES,
        ("A", "B", 5),
        ("C", "G", 6),
    )
    best_cost, best_pair, best_tree = best_single_weight_swap(
        CABLE_NETWORK_VERTICES,
        CABLE_NETWORK_EDGES,
    )
    return {
        "example_swap": example_swap,
        "best_cost": best_cost,
        "best_pair": best_pair,
        "best_tree": best_tree,
    }

