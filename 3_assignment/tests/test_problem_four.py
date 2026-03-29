from dat600_assignment.solutions import solve_problem_four


def test_negative_edge_counterexample_breaks_dijkstra() -> None:
    solution = solve_problem_four()

    assert solution.dijkstra_distances == {"s": 0, "a": 1, "b": 4, "c": 3}
    assert solution.bellman_ford_distances == {"s": 0, "a": -1, "b": 4, "c": 1}

    assert solution.dijkstra_paths["a"] == ("s", "a")
    assert solution.bellman_ford_paths["a"] == ("s", "b", "a")
    assert solution.dijkstra_paths["c"] == ("s", "a", "c")
    assert solution.bellman_ford_paths["c"] == ("s", "b", "a", "c")

