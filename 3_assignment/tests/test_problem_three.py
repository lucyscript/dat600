from dat600_assignment.solutions import solve_problem_three


def test_champions_and_groups() -> None:
    solution = solve_problem_three()

    assert solution.champions == ("A", "B", "D")
    assert solution.groups == (("A", "B", "D"), ("C",), ("E", "F", "G"))

