from dat600_assignment.solutions import solve_problem_two


def test_cable_network_mst_cost() -> None:
    solution = solve_problem_two()

    assert solution.mst.cost == 26
    assert solution.mst.edges == (
        ("A", "D", 1),
        ("C", "D", 2),
        ("D", "E", 2),
        ("B", "D", 4),
        ("D", "F", 4),
        ("C", "G", 6),
        ("F", "H", 7),
    )
    assert solution.within_budget_30 is True


def test_degree_limit_on_d_makes_budget_30_impossible() -> None:
    solution = solve_problem_two()

    assert solution.degree_constrained_exact.cost == 31
    assert solution.degree_constrained_exact.edges == (
        ("A", "D", 1),
        ("C", "D", 2),
        ("D", "E", 2),
        ("A", "B", 5),
        ("C", "G", 6),
        ("F", "H", 7),
        ("B", "H", 8),
    )
    assert solution.degree_constrained_exact.degree_by_vertex["D"] == 3
    assert solution.degree_constrained_heuristic.cost == 31
    assert solution.within_budget_30_with_degree_limit is False


def test_degree_aware_kruskal_is_not_globally_optimal() -> None:
    solution = solve_problem_two()

    assert solution.counterexample_heuristic.cost == 13
    assert solution.counterexample_optimal.cost == 12


def test_single_weight_swap_can_meet_budget_25() -> None:
    solution = solve_problem_two()

    assert solution.example_swap_result.cost == 25
    assert solution.best_swap_cost == 24
    assert solution.best_swap_pair == (("A", "D", 1), ("F", "H", 7))
    assert solution.best_swap_tree.cost == 24

