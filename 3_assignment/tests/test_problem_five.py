from dat600_assignment.solutions import solve_problem_five


def test_antiparallel_resolution_and_max_flow() -> None:
    solution = solve_problem_five()

    assert solution.resolved_graph_has_antiparallel_edges is False
    assert ("V3", "V3_to_V1", 6) in solution.resolved_antiparallel_edges
    assert ("V3_to_V1", "V1", 6) in solution.resolved_antiparallel_edges

    assert solution.max_flow.value == 30
    assert tuple(step.path for step in solution.max_flow.steps) == (
        ("s", "V1", "V4", "t"),
        ("s", "V2", "V5", "t"),
        ("s", "V2", "V3", "V5", "t"),
        ("s", "V2", "V3", "V1", "V4", "t"),
    )
    assert tuple(step.bottleneck for step in solution.max_flow.steps) == (14, 7, 3, 6)
    assert solution.transformed_max_flow.value == 30
    assert solution.max_flow.min_cut_edges == (("V4", "t", 20), ("V5", "t", 10))
