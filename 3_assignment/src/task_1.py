"""Task 1: basic graph operations and traversals."""

from __future__ import annotations

from algorithms import (
    adjacency_list_from_matrix,
    bfs_with_timestamps,
    dfs_with_timestamps,
    directed_edges_from_adjacency_list,
    is_dag,
    topological_sort,
    transform_to_dag,
)
from assignment_data import (
    ADJACENCY_MATRIX,
    ADJACENCY_MATRIX_LABELS,
    FIGURE_1_GRAPH,
    FIGURE_1_WITH_EXTRA_EDGES,
)


def solve_task_1a_matrix() -> dict[str, object]:
    adjacency_list = adjacency_list_from_matrix(ADJACENCY_MATRIX_LABELS, ADJACENCY_MATRIX)
    return {
        "adjacency_list": adjacency_list,
        "edges": directed_edges_from_adjacency_list(adjacency_list),
    }


def solve_task_1a_figure() -> dict[str, object]:
    return {"adjacency_list": {node: list(neighbors) for node, neighbors in FIGURE_1_GRAPH.items()}}


def solve_task_1b() -> dict[str, object]:
    return {
        "dfs": dfs_with_timestamps(FIGURE_1_GRAPH, "A"),
        "bfs": bfs_with_timestamps(FIGURE_1_GRAPH, "A"),
    }


def solve_task_1c() -> dict[str, object]:
    removed_edge = ("F", "B")
    dag_graph = {
        node: [neighbor for neighbor in neighbors if (node, neighbor) != removed_edge]
        for node, neighbors in FIGURE_1_GRAPH.items()
    }
    return {
        "removed_edge": removed_edge,
        "topological_order": topological_sort(dag_graph),
    }


def solve_task_1d() -> dict[str, object]:
    dag_graph, removed_edges = transform_to_dag(FIGURE_1_WITH_EXTRA_EDGES)
    return {
        "removed_edges": removed_edges,
        "is_dag": is_dag(dag_graph),
    }

