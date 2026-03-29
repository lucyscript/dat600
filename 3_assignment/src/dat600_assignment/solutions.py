"""Computed answers for the assignment."""

from __future__ import annotations

from dataclasses import dataclass

from .algorithms import (
    adjacency_list_from_matrix,
    bellman_ford_shortest_paths,
    best_single_weight_swap,
    bfs_with_timestamps,
    degree_constrained_kruskal,
    dfs_with_timestamps,
    dijkstra_shortest_paths,
    directed_edges_from_adjacency_list,
    edmonds_karp,
    exact_degree_constrained_spanning_tree,
    example_single_weight_swap,
    find_champions,
    has_antiparallel_edges,
    is_dag,
    kruskal_mst,
    reconstruct_path,
    resolve_antiparallel_edges,
    strongly_connected_components,
    topological_sort,
    transform_to_dag,
)
from .assignment_data import (
    ADJACENCY_MATRIX,
    ADJACENCY_MATRIX_LABELS,
    CABLE_NETWORK_EDGES,
    CABLE_NETWORK_VERTICES,
    DEGREE_LIMIT_COUNTEREXAMPLE_EDGES,
    DEGREE_LIMIT_COUNTEREXAMPLE_LIMITS,
    DEGREE_LIMIT_COUNTEREXAMPLE_VERTICES,
    FIGURE_1_GRAPH,
    FIGURE_1_WITH_EXTRA_EDGES,
    FINDING_CHAMPION_GRAPH,
    MAX_FLOW_EDGES,
    NEGATIVE_EDGE_COUNTEREXAMPLE,
)


@dataclass(frozen=True)
class ProblemOneSolution:
    matrix_adjacency_list: dict[str, list[str]]
    matrix_graph_edges: tuple[tuple[str, str], ...]
    figure_adjacency_list: dict[str, list[str]]
    dfs: object
    bfs: object
    dag_removed_edge: tuple[str, str]
    dag_topological_order: tuple[str, ...]
    general_dag_removed_edges: tuple[tuple[str, str], ...]
    general_dag_graph_is_dag: bool


@dataclass(frozen=True)
class ProblemTwoSolution:
    mst: object
    within_budget_30: bool
    degree_constrained_exact: object
    degree_constrained_heuristic: object
    within_budget_30_with_degree_limit: bool
    counterexample_heuristic: object
    counterexample_optimal: object
    example_swap_result: object
    best_swap_cost: int
    best_swap_pair: tuple[tuple[str, str, int], tuple[str, str, int]]
    best_swap_tree: object


@dataclass(frozen=True)
class ProblemThreeSolution:
    champions: tuple[str, ...]
    groups: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class ProblemFourSolution:
    dijkstra_distances: dict[str, int]
    dijkstra_paths: dict[str, tuple[str, ...]]
    bellman_ford_distances: dict[str, int]
    bellman_ford_paths: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class ProblemFiveSolution:
    resolved_antiparallel_edges: tuple[tuple[str, str, int], ...]
    resolved_graph_has_antiparallel_edges: bool
    max_flow: object
    transformed_max_flow: object


def solve_problem_one() -> ProblemOneSolution:
    matrix_adjacency_list = adjacency_list_from_matrix(ADJACENCY_MATRIX_LABELS, ADJACENCY_MATRIX)
    dfs_result = dfs_with_timestamps(FIGURE_1_GRAPH, "A")
    bfs_result = bfs_with_timestamps(FIGURE_1_GRAPH, "A")
    dag_removed_edge = ("F", "B")
    dag_graph = {
        node: [neighbor for neighbor in neighbors if (node, neighbor) != dag_removed_edge]
        for node, neighbors in FIGURE_1_GRAPH.items()
    }
    transformed_graph, removed_edges = transform_to_dag(FIGURE_1_WITH_EXTRA_EDGES)
    return ProblemOneSolution(
        matrix_adjacency_list=matrix_adjacency_list,
        matrix_graph_edges=directed_edges_from_adjacency_list(matrix_adjacency_list),
        figure_adjacency_list={node: list(neighbors) for node, neighbors in FIGURE_1_GRAPH.items()},
        dfs=dfs_result,
        bfs=bfs_result,
        dag_removed_edge=dag_removed_edge,
        dag_topological_order=topological_sort(dag_graph),
        general_dag_removed_edges=removed_edges,
        general_dag_graph_is_dag=is_dag(transformed_graph),
    )


def solve_problem_two() -> ProblemTwoSolution:
    mst_result = kruskal_mst(CABLE_NETWORK_VERTICES, CABLE_NETWORK_EDGES)
    degree_limits = {"D": 3}
    exact_result = exact_degree_constrained_spanning_tree(
        CABLE_NETWORK_VERTICES,
        CABLE_NETWORK_EDGES,
        degree_limits,
    )
    heuristic_result = degree_constrained_kruskal(
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
    example_swap_result = example_single_weight_swap(
        CABLE_NETWORK_VERTICES,
        CABLE_NETWORK_EDGES,
        ("A", "B", 5),
        ("C", "G", 6),
    )
    best_swap_cost, best_swap_pair, best_swap_tree = best_single_weight_swap(
        CABLE_NETWORK_VERTICES,
        CABLE_NETWORK_EDGES,
    )
    return ProblemTwoSolution(
        mst=mst_result,
        within_budget_30=mst_result.cost <= 30,
        degree_constrained_exact=exact_result,
        degree_constrained_heuristic=heuristic_result,
        within_budget_30_with_degree_limit=exact_result.cost <= 30,
        counterexample_heuristic=counterexample_heuristic,
        counterexample_optimal=counterexample_optimal,
        example_swap_result=example_swap_result,
        best_swap_cost=best_swap_cost,
        best_swap_pair=best_swap_pair,
        best_swap_tree=best_swap_tree,
    )


def solve_problem_three() -> ProblemThreeSolution:
    return ProblemThreeSolution(
        champions=find_champions(FINDING_CHAMPION_GRAPH),
        groups=strongly_connected_components(FINDING_CHAMPION_GRAPH),
    )


def solve_problem_four() -> ProblemFourSolution:
    dijkstra_distances, dijkstra_previous = dijkstra_shortest_paths(NEGATIVE_EDGE_COUNTEREXAMPLE, "s")
    bellman_distances, bellman_previous = bellman_ford_shortest_paths(NEGATIVE_EDGE_COUNTEREXAMPLE, "s")
    vertices = tuple(NEGATIVE_EDGE_COUNTEREXAMPLE)
    return ProblemFourSolution(
        dijkstra_distances=dijkstra_distances,
        dijkstra_paths={vertex: reconstruct_path(dijkstra_previous, vertex) for vertex in vertices},
        bellman_ford_distances=bellman_distances,
        bellman_ford_paths={vertex: reconstruct_path(bellman_previous, vertex) for vertex in vertices},
    )


def solve_problem_five() -> ProblemFiveSolution:
    resolved_edges = resolve_antiparallel_edges(MAX_FLOW_EDGES)
    return ProblemFiveSolution(
        resolved_antiparallel_edges=resolved_edges,
        resolved_graph_has_antiparallel_edges=has_antiparallel_edges(resolved_edges),
        max_flow=edmonds_karp(MAX_FLOW_EDGES, "s", "t"),
        transformed_max_flow=edmonds_karp(resolved_edges, "s", "t"),
    )


def solve_all() -> tuple[
    ProblemOneSolution,
    ProblemTwoSolution,
    ProblemThreeSolution,
    ProblemFourSolution,
    ProblemFiveSolution,
]:
    return (
        solve_problem_one(),
        solve_problem_two(),
        solve_problem_three(),
        solve_problem_four(),
        solve_problem_five(),
    )

