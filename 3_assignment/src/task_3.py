"""Task 3: champion finding and SCC grouping."""

from __future__ import annotations

from algorithms import find_champions, strongly_connected_components
from assignment_data import FINDING_CHAMPION_GRAPH


def solve_task_3a() -> dict[str, object]:
    return {"champions": find_champions(FINDING_CHAMPION_GRAPH)}


def solve_task_3b() -> dict[str, object]:
    return {"groups": strongly_connected_components(FINDING_CHAMPION_GRAPH)}

