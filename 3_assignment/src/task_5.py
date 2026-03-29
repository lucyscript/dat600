"""Task 5: maximum-flow analysis."""

from __future__ import annotations

from algorithms import edmonds_karp, has_antiparallel_edges, resolve_antiparallel_edges
from assignment_data import MAX_FLOW_EDGES


def solve_task_5a() -> dict[str, object]:
    resolved_edges = resolve_antiparallel_edges(MAX_FLOW_EDGES)
    return {
        "resolved_edges": resolved_edges,
        "has_antiparallel_edges": has_antiparallel_edges(resolved_edges),
    }


def solve_task_5b() -> dict[str, object]:
    return {"max_flow": edmonds_karp(MAX_FLOW_EDGES, "s", "t")}


def solve_task_5c() -> dict[str, object]:
    max_flow = edmonds_karp(MAX_FLOW_EDGES, "s", "t")
    return {
        "min_cut_source_side": max_flow.min_cut_source_side,
        "min_cut_edges": max_flow.min_cut_edges,
        "cut_capacity": sum(weight for _, _, weight in max_flow.min_cut_edges),
    }


def solve_task_5d() -> dict[str, object]:
    return {
        "running_time": "O(E * |f*|)",
        "improvement": "Edmonds-Karp or Dinic",
    }
