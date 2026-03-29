"""Static graph data taken from the assignment PDF."""

from __future__ import annotations

from collections.abc import Mapping, Sequence


ADJACENCY_MATRIX_LABELS: list[str] = ["1", "2", "3", "4", "5", "6"]

ADJACENCY_MATRIX: list[list[int]] = [
    [0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0],
    [1, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
]

FIGURE_1_GRAPH: dict[str, list[str]] = {
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

FIGURE_1_WITH_EXTRA_EDGES: dict[str, list[str]] = {
    "A": ["B"],
    "B": ["C", "D"],
    "C": ["A", "E", "F"],
    "D": ["E", "F"],
    "E": ["F", "G", "J"],
    "F": ["B", "G", "H", "J"],
    "G": [],
    "H": ["I"],
    "I": ["C"],
    "J": ["I"],
}

CABLE_NETWORK_VERTICES: list[str] = ["A", "B", "C", "D", "E", "F", "G", "H"]

CABLE_NETWORK_EDGES: list[tuple[str, str, int]] = [
    ("A", "D", 1),
    ("C", "D", 2),
    ("D", "E", 2),
    ("B", "D", 4),
    ("D", "F", 4),
    ("A", "B", 5),
    ("C", "G", 6),
    ("F", "H", 7),
    ("B", "H", 8),
    ("E", "H", 8),
    ("F", "G", 9),
]

FINDING_CHAMPION_GRAPH: dict[str, list[str]] = {
    "A": ["B", "D"],
    "B": ["A", "C"],
    "C": ["E", "F"],
    "D": ["B", "C"],
    "E": ["G"],
    "F": ["E"],
    "G": ["F"],
}

NEGATIVE_EDGE_COUNTEREXAMPLE: dict[str, list[tuple[str, int]]] = {
    "s": [("a", 1), ("b", 4)],
    "a": [("c", 2)],
    "b": [("a", -5), ("c", 3)],
    "c": [],
}

MAX_FLOW_EDGES: list[tuple[str, str, int]] = [
    ("s", "V1", 14),
    ("s", "V2", 25),
    ("V1", "V4", 21),
    ("V1", "V3", 3),
    ("V3", "V1", 6),
    ("V2", "V3", 13),
    ("V2", "V5", 7),
    ("V4", "V3", 10),
    ("V3", "V5", 15),
    ("V5", "V4", 5),
    ("V4", "t", 20),
    ("V5", "t", 10),
]

DEGREE_LIMIT_COUNTEREXAMPLE_VERTICES: list[str] = ["A", "B", "C", "D", "E"]
DEGREE_LIMIT_COUNTEREXAMPLE_EDGES: list[tuple[str, str, int]] = [
    ("C", "E", 1),
    ("D", "E", 2),
    ("A", "D", 3),
    ("B", "D", 4),
    ("A", "C", 5),
    ("A", "E", 6),
    ("B", "C", 7),
    ("B", "E", 8),
    ("A", "B", 9),
    ("C", "D", 5),
]
DEGREE_LIMIT_COUNTEREXAMPLE_LIMITS: dict[str, int] = {"D": 2}


def sorted_graph(graph: Mapping[str, Sequence[str]]) -> dict[str, list[str]]:
    """Return a copy with nodes and neighbors in alphabetical order."""

    return {node: sorted(neighbors) for node, neighbors in sorted(graph.items())}

