from dat600_assignment.algorithms import is_dag, remove_edges
from dat600_assignment.assignment_data import FIGURE_1_GRAPH
from dat600_assignment.solutions import solve_problem_one


def test_matrix_adjacency_list_and_edges() -> None:
    solution = solve_problem_one()

    assert solution.matrix_adjacency_list == {
        "1": ["2"],
        "2": ["2", "3", "4"],
        "3": ["1", "2", "5"],
        "4": ["5", "6"],
        "5": ["3", "4"],
        "6": ["4"],
    }
    assert solution.matrix_graph_edges == (
        ("1", "2"),
        ("2", "2"),
        ("2", "3"),
        ("2", "4"),
        ("3", "1"),
        ("3", "2"),
        ("3", "5"),
        ("4", "5"),
        ("4", "6"),
        ("5", "3"),
        ("5", "4"),
        ("6", "4"),
    )


def test_figure_one_adjacency_list() -> None:
    solution = solve_problem_one()

    assert solution.figure_adjacency_list == {
        "A": ["B"],
        "B": ["C", "D"],
        "C": ["E", "F"],
        "D": ["E", "F"],
        "E": ["F", "G", "J"],
        "F": ["B", "G", "H", "J"],
        "G": [],
        "H": ["I"],
        "I": [],
        "J": ["I"],
    }


def test_dfs_and_bfs_from_a() -> None:
    solution = solve_problem_one()

    assert solution.dfs.discover == {
        "A": 1,
        "B": 2,
        "C": 3,
        "E": 4,
        "F": 5,
        "G": 6,
        "H": 8,
        "I": 9,
        "J": 12,
        "D": 17,
    }
    assert solution.dfs.finish == {
        "G": 7,
        "I": 10,
        "H": 11,
        "J": 13,
        "F": 14,
        "E": 15,
        "C": 16,
        "D": 18,
        "B": 19,
        "A": 20,
    }
    assert solution.dfs.parent == {
        "A": None,
        "B": "A",
        "C": "B",
        "D": "B",
        "E": "C",
        "F": "E",
        "G": "F",
        "H": "F",
        "I": "H",
        "J": "F",
    }

    assert solution.bfs.distances == {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 2,
        "E": 3,
        "F": 3,
        "G": 4,
        "H": 4,
        "I": 5,
        "J": 4,
    }
    assert solution.bfs.discover == {
        "A": 1,
        "B": 2,
        "C": 4,
        "D": 5,
        "E": 7,
        "F": 8,
        "G": 11,
        "J": 12,
        "H": 14,
        "I": 17,
    }
    assert solution.bfs.finish == {
        "A": 3,
        "B": 6,
        "C": 9,
        "D": 10,
        "E": 13,
        "F": 15,
        "G": 16,
        "J": 18,
        "H": 19,
        "I": 20,
    }


def test_removing_f_to_b_makes_figure_one_a_dag() -> None:
    solution = solve_problem_one()
    dag_graph = remove_edges(FIGURE_1_GRAPH, [solution.dag_removed_edge])

    assert solution.dag_removed_edge == ("F", "B")
    assert is_dag(dag_graph) is True
    assert solution.dag_topological_order == ("A", "B", "C", "D", "E", "F", "G", "H", "J", "I")


def test_general_transformation_removes_back_edges() -> None:
    solution = solve_problem_one()

    assert solution.general_dag_removed_edges == (("C", "A"), ("F", "B"), ("I", "C"))
    assert solution.general_dag_graph_is_dag is True

