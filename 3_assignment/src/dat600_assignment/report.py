"""Render the computed solutions as Org mode."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from .solutions import solve_all


def format_adjacency_list(graph: Mapping[str, Sequence[str]]) -> str:
    lines = []
    for node, neighbors in graph.items():
        lines.append(f"- ~{node}~: [{', '.join(neighbors)}]")
    return "\n".join(lines)


def format_edges(edges: Sequence[tuple[str, str]]) -> str:
    return ", ".join(rf"\(({source}, {target})\)" for source, target in edges)


def format_weighted_edges(edges: Sequence[tuple[str, str, int]]) -> str:
    return ", ".join(rf"\(({left}, {right}, {weight})\)" for left, right, weight in edges)


def format_set(items: Sequence[str]) -> str:
    return r"\{" + ", ".join(items) + r"\}"


def format_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    header_row = "| " + " | ".join(str(header) for header in headers) + " |"
    separator = "|" + "+".join("-" * (len(str(header)) + 2) for header in headers) + "|"
    body_rows = [
        "| " + " | ".join("" if value is None else str(value) for value in row) + " |"
        for row in rows
    ]
    return "\n".join([header_row, separator, *body_rows])


def render_org() -> str:
    problem_one, problem_two, problem_three, problem_four, problem_five = solve_all()

    dfs_rows = [
        (
            vertex,
            problem_one.dfs.parent[vertex],
            problem_one.dfs.discover[vertex],
            problem_one.dfs.finish[vertex],
        )
        for vertex in sorted(problem_one.dfs.discover, key=problem_one.dfs.discover.get)
    ]
    bfs_rows = [
        (
            vertex,
            problem_one.bfs.parent[vertex],
            problem_one.bfs.distances[vertex],
            problem_one.bfs.discover[vertex],
            problem_one.bfs.finish[vertex],
        )
        for vertex in sorted(problem_one.bfs.discover, key=problem_one.bfs.discover.get)
    ]
    shortest_path_rows = [
        (
            vertex,
            problem_four.dijkstra_distances[vertex],
            " -> ".join(problem_four.dijkstra_paths[vertex]),
            problem_four.bellman_ford_distances[vertex],
            " -> ".join(problem_four.bellman_ford_paths[vertex]),
        )
        for vertex in ("s", "a", "b", "c")
    ]
    flow_rows = [
        (" -> ".join(step.path), step.bottleneck, step.total_flow)
        for step in problem_five.max_flow.steps
    ]

    sections = [
        "#+TITLE: DAT600 Assignment 3-4 Solution",
        "#+OPTIONS: toc:nil num:t",
        "",
        "* Problem Basic Graph",
        "** a.1 Adjacency list from the matrix",
        format_adjacency_list(problem_one.matrix_adjacency_list),
        "",
        "** a.2 Graph form of the adjacency matrix",
        "The directed edge set is:",
        format_edges(problem_one.matrix_graph_edges) + ".",
        "This is the graph-form representation of the matrix.",
        "",
        "** a.3 Adjacency list for Figure 1",
        format_adjacency_list(problem_one.figure_adjacency_list),
        "",
        "** b. DFS from A",
        f"Visit order: {' -> '.join(problem_one.dfs.order)}.",
        format_table(["Vertex", "Parent", "Start", "Finish"], dfs_rows),
        "",
        "** b. BFS from A",
        "For BFS, Start is the discovery time and Finish is the time when the adjacency list has been fully processed.",
        f"Dequeue order: {' -> '.join(problem_one.bfs.order)}.",
        format_table(["Vertex", "Parent", "Distance", "Start", "Finish"], bfs_rows),
        "",
        "Queue snapshots:",
        *[f"- {snapshot}" for snapshot in problem_one.bfs.queue_snapshots or []],
        "",
        "** c. Remove one edge to get a DAG",
        rf"Removing \(({problem_one.dag_removed_edge[0]}, {problem_one.dag_removed_edge[1]})\) breaks every directed cycle in Figure 1.",
        f"One alphabetical topological order is {' -> '.join(problem_one.dag_topological_order)}.",
        "",
        "** d. General algorithm to transform a directed graph into a DAG",
        "Run DFS and remove every back edge. In a directed graph, cycles appear exactly when DFS encounters a back edge, so removing all back edges leaves a DAG.",
        rf"On Figure 1 plus \(I \rightarrow C\) and \(C \rightarrow A\), the removed back edges are {format_edges(problem_one.general_dag_removed_edges)}.",
        f"The resulting graph is a DAG: {problem_one.general_dag_graph_is_dag}.",
        r"Running time: \(O(V + E)\).",
        "",
        "* Problem Cable Network",
        r"** a. Budget \(b = 30\)",
        rf"The MST has cost \( {problem_two.mst.cost} \) with edges {format_weighted_edges(problem_two.mst.edges)}.",
        f"So the answer is {problem_two.within_budget_30}.",
        "",
        "** b. Degree limit on D",
        rf"With the additional constraint \(deg(D) \le 3\), the cheapest feasible spanning tree has cost \( {problem_two.degree_constrained_exact.cost} \) with edges {format_weighted_edges(problem_two.degree_constrained_exact.edges)}.",
        (
            r"The budget \(30\) is still achievable."
            if problem_two.within_budget_30_with_degree_limit
            else r"The budget \(30\) is not achievable."
        ),
        "A degree-aware Kruskal heuristic returns:",
        f"- Cost {problem_two.degree_constrained_heuristic.cost}",
        f"- Edges {format_weighted_edges(problem_two.degree_constrained_heuristic.edges)}",
        "This heuristic is not always globally optimal.",
        rf"The counterexample heuristic cost is \( {problem_two.counterexample_heuristic.cost} \) with edges {format_weighted_edges(problem_two.counterexample_heuristic.edges)}.",
        rf"The counterexample optimal cost is \( {problem_two.counterexample_optimal.cost} \) with edges {format_weighted_edges(problem_two.counterexample_optimal.edges)}.",
        "",
        r"** c. One weight swap under budget \(b' = 25\)",
        rf"Yes. Swapping \((A, B, 5)\) with \((C, G, 6)\) yields an MST of cost \( {problem_two.example_swap_result.cost} \).",
        rf"The best single swap found by exhaustive search gives cost \( {problem_two.best_swap_cost} \) by swapping {format_weighted_edges(problem_two.best_swap_pair)}.",
        "",
        "* Problem Finding Champion",
        "** a. Champions",
        rf"The champions are \({', '.join(problem_three.champions)}\).",
        "Algorithm: compute SCCs, compress the graph to a DAG, and check whether there is a unique source SCC that can reach every SCC. Every node in that SCC is a champion.",
        r"Running time: \(O(V + E)\).",
        "",
        "** b. Groups of mutually defeating nodes",
        rf"The groups are \( {', '.join(format_set(group) for group in problem_three.groups)} \).",
        "These groups are exactly the strongly connected components.",
        r"Running time: \(O(V + E)\).",
        "",
        "* Problem Shortest Path",
        r"Use the graph with edges \(s \rightarrow a\) (1), \(s \rightarrow b\) (4), \(b \rightarrow a\) (-5), \(a \rightarrow c\) (2), \(b \rightarrow c\) (3).",
        "",
        "** a. Correct result vs. Dijkstra",
        format_table(
            ["Vertex", "Dijkstra distance", "Dijkstra path", "Bellman-Ford distance", "Bellman-Ford path"],
            shortest_path_rows,
        ),
        r"Dijkstra finalizes \(a\) too early with distance \(1\), so it misses the better path \(s \rightarrow b \rightarrow a\) with length \(-1\). It therefore also reports the wrong value for \(c\).",
        "",
        "** b. Fix for negative edges",
        "Use Bellman-Ford for single-source shortest paths when negative edges are allowed and negative cycles are excluded.",
        r"Running time: \(O(VE)\).",
        "",
        "* Problem Maximum Flow",
        "** a. Resolving the antiparallel edge",
        r"The antiparallel pair is \(V1 \rightarrow V3\) and \(V3 \rightarrow V1\).",
        r"Replace \(V3 \rightarrow V1\) (6) with \(V3 \rightarrow V3\_to\_V1\) (6) and \(V3\_to\_V1 \rightarrow V1\) (6).",
        f"The transformed network still has antiparallel edges: {problem_five.resolved_graph_has_antiparallel_edges}.",
        "",
        "** b. Ford-Fulkerson walkthrough",
        format_table(["Augmenting path", "Bottleneck", "Total flow"], flow_rows),
        rf"The maximum flow is \( {problem_five.max_flow.value} \).",
        "",
        "** c. Bottleneck via cuts",
        rf"A minimum cut is \(S = {format_set(sorted(problem_five.max_flow.min_cut_source_side))}\) and \(T = \{{t\}}\).",
        rf"The cut edges are {format_weighted_edges(problem_five.max_flow.min_cut_edges)}, for total capacity \( {sum(weight for _, _, weight in problem_five.max_flow.min_cut_edges)} \).",
        "Because the cut capacity equals the max flow value, this cut is the bottleneck.",
        "",
        "** d. Running time and improvement",
        r"Ford-Fulkerson runs in \(O(E \cdot |f^\ast|)\) for integral capacities, where \(|f^\ast|\) is the value of the maximum flow.",
        r"A standard improvement is Edmonds-Karp, which always picks the shortest augmenting path with BFS and runs in \(O(VE^2)\).",
        "For larger networks, Dinic is usually faster in practice.",
    ]
    return "\n".join(sections)
