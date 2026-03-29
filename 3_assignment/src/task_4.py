"""Task 4: negative-edge shortest-path counterexample."""

from __future__ import annotations

from algorithms import bellman_ford_shortest_paths, dijkstra_shortest_paths, reconstruct_path
from assignment_data import NEGATIVE_EDGE_COUNTEREXAMPLE


def solve_task_4a() -> dict[str, object]:
    dijkstra_distances, dijkstra_previous = dijkstra_shortest_paths(NEGATIVE_EDGE_COUNTEREXAMPLE, "s")
    bellman_distances, bellman_previous = bellman_ford_shortest_paths(NEGATIVE_EDGE_COUNTEREXAMPLE, "s")
    vertices = tuple(NEGATIVE_EDGE_COUNTEREXAMPLE)
    return {
        "dijkstra_distances": dijkstra_distances,
        "dijkstra_paths": {vertex: reconstruct_path(dijkstra_previous, vertex) for vertex in vertices},
        "bellman_ford_distances": bellman_distances,
        "bellman_ford_paths": {vertex: reconstruct_path(bellman_previous, vertex) for vertex in vertices},
    }


def solve_task_4b() -> dict[str, object]:
    return {
        "algorithm": "Bellman-Ford",
        "running_time": "O(VE)",
    }

