"""Shared graph algorithms for the assignment tasks."""

from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from heapq import heapify, heappop, heappush
from itertools import combinations


Node = str
WeightedEdge = tuple[Node, Node, int]
WeightedGraph = dict[Node, list[tuple[Node, int]]]
AdjacencyList = dict[Node, list[Node]]


@dataclass(frozen=True)
class TraversalResult:
    discover: dict[Node, int]
    finish: dict[Node, int]
    parent: dict[Node, Node | None]
    order: list[Node]
    distances: dict[Node, int | None] | None = None
    queue_snapshots: list[str] | None = None


@dataclass(frozen=True)
class SpanningTreeResult:
    cost: int
    edges: tuple[WeightedEdge, ...]
    degree_by_vertex: dict[Node, int]


@dataclass(frozen=True)
class FlowStep:
    path: tuple[Node, ...]
    bottleneck: int
    total_flow: int


@dataclass(frozen=True)
class MaxFlowResult:
    value: int
    steps: tuple[FlowStep, ...]
    min_cut_source_side: frozenset[Node]
    min_cut_edges: tuple[WeightedEdge, ...]


class UnionFind:
    def __init__(self, vertices: Iterable[Node]) -> None:
        self.parent = {vertex: vertex for vertex in vertices}

    def find(self, vertex: Node) -> Node:
        while self.parent[vertex] != vertex:
            self.parent[vertex] = self.parent[self.parent[vertex]]
            vertex = self.parent[vertex]
        return vertex

    def union(self, left: Node, right: Node) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        self.parent[right_root] = left_root
        return True


def normalize_adjacency_list(graph: Mapping[Node, Sequence[Node]]) -> AdjacencyList:
    return {node: sorted(neighbors) for node, neighbors in sorted(graph.items())}


def adjacency_list_from_matrix(labels: Sequence[Node], matrix: Sequence[Sequence[int]]) -> AdjacencyList:
    adjacency_list: AdjacencyList = {}
    for row_index, label in enumerate(labels):
        adjacency_list[label] = [
            labels[column_index]
            for column_index, edge in enumerate(matrix[row_index])
            if edge
        ]
    return normalize_adjacency_list(adjacency_list)


def directed_edges_from_adjacency_list(graph: Mapping[Node, Sequence[Node]]) -> tuple[tuple[Node, Node], ...]:
    return tuple(
        (source, target)
        for source, neighbors in normalize_adjacency_list(graph).items()
        for target in neighbors
    )


def dfs_with_timestamps(graph: Mapping[Node, Sequence[Node]], start: Node) -> TraversalResult:
    adjacency = normalize_adjacency_list(graph)
    color = {vertex: "white" for vertex in adjacency}
    parent: dict[Node, Node | None] = {vertex: None for vertex in adjacency}
    discover: dict[Node, int] = {}
    finish: dict[Node, int] = {}
    order: list[Node] = []
    time = 0

    def visit(vertex: Node) -> None:
        nonlocal time
        color[vertex] = "gray"
        time += 1
        discover[vertex] = time
        order.append(vertex)
        for neighbor in adjacency[vertex]:
            if color[neighbor] == "white":
                parent[neighbor] = vertex
                visit(neighbor)
        color[vertex] = "black"
        time += 1
        finish[vertex] = time

    visit(start)
    for vertex in adjacency:
        if color[vertex] == "white":
            visit(vertex)
    return TraversalResult(discover=discover, finish=finish, parent=parent, order=order)


def bfs_with_timestamps(graph: Mapping[Node, Sequence[Node]], start: Node) -> TraversalResult:
    adjacency = normalize_adjacency_list(graph)
    state = {vertex: "white" for vertex in adjacency}
    parent: dict[Node, Node | None] = {vertex: None for vertex in adjacency}
    discover: dict[Node, int] = {}
    finish: dict[Node, int] = {}
    distances: dict[Node, int | None] = {vertex: None for vertex in adjacency}
    order: list[Node] = []
    queue_snapshots: list[str] = []
    time = 0
    queue: deque[Node] = deque([start])
    state[start] = "gray"
    distances[start] = 0
    time += 1
    discover[start] = time

    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        queue_snapshots.append(f"pop {vertex}: [{', '.join(queue)}]")
        for neighbor in adjacency[vertex]:
            if state[neighbor] == "white":
                state[neighbor] = "gray"
                parent[neighbor] = vertex
                distances[neighbor] = distances[vertex] + 1 if distances[vertex] is not None else None
                queue.append(neighbor)
                time += 1
                discover[neighbor] = time
                queue_snapshots.append(f"discover {neighbor} from {vertex}: [{', '.join(queue)}]")
        state[vertex] = "black"
        time += 1
        finish[vertex] = time

    return TraversalResult(
        discover=discover,
        finish=finish,
        parent=parent,
        order=order,
        distances=distances,
        queue_snapshots=queue_snapshots,
    )


def remove_edges(graph: Mapping[Node, Sequence[Node]], edges_to_remove: Iterable[tuple[Node, Node]]) -> AdjacencyList:
    removal_set = set(edges_to_remove)
    return {
        node: [neighbor for neighbor in sorted(neighbors) if (node, neighbor) not in removal_set]
        for node, neighbors in normalize_adjacency_list(graph).items()
    }


def find_back_edges(graph: Mapping[Node, Sequence[Node]]) -> tuple[tuple[Node, Node], ...]:
    adjacency = normalize_adjacency_list(graph)
    color = {vertex: "white" for vertex in adjacency}
    back_edges: list[tuple[Node, Node]] = []

    def visit(vertex: Node) -> None:
        color[vertex] = "gray"
        for neighbor in adjacency[vertex]:
            if color[neighbor] == "gray":
                back_edges.append((vertex, neighbor))
            elif color[neighbor] == "white":
                visit(neighbor)
        color[vertex] = "black"

    for vertex in adjacency:
        if color[vertex] == "white":
            visit(vertex)
    return tuple(back_edges)


def transform_to_dag(graph: Mapping[Node, Sequence[Node]]) -> tuple[AdjacencyList, tuple[tuple[Node, Node], ...]]:
    back_edges = find_back_edges(graph)
    return remove_edges(graph, back_edges), back_edges


def topological_sort(graph: Mapping[Node, Sequence[Node]]) -> tuple[Node, ...]:
    adjacency = normalize_adjacency_list(graph)
    indegree = {vertex: 0 for vertex in adjacency}
    for neighbors in adjacency.values():
        for neighbor in neighbors:
            indegree[neighbor] += 1

    available = [vertex for vertex, degree in indegree.items() if degree == 0]
    heapify(available)
    order: list[Node] = []

    while available:
        vertex = heappop(available)
        order.append(vertex)
        for neighbor in adjacency[vertex]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                heappush(available, neighbor)

    if len(order) != len(adjacency):
        raise ValueError("graph contains a cycle")
    return tuple(order)


def is_dag(graph: Mapping[Node, Sequence[Node]]) -> bool:
    try:
        topological_sort(graph)
        return True
    except ValueError:
        return False


def reverse_graph(graph: Mapping[Node, Sequence[Node]]) -> AdjacencyList:
    reversed_graph = {vertex: [] for vertex in graph}
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            reversed_graph[neighbor].append(vertex)
    return normalize_adjacency_list(reversed_graph)


def strongly_connected_components(graph: Mapping[Node, Sequence[Node]]) -> tuple[tuple[Node, ...], ...]:
    adjacency = normalize_adjacency_list(graph)
    reversed_adjacency = reverse_graph(adjacency)
    visited: set[Node] = set()
    finish_order: list[Node] = []

    def first_pass(vertex: Node) -> None:
        visited.add(vertex)
        for neighbor in adjacency[vertex]:
            if neighbor not in visited:
                first_pass(neighbor)
        finish_order.append(vertex)

    for vertex in adjacency:
        if vertex not in visited:
            first_pass(vertex)

    visited.clear()
    components: list[tuple[Node, ...]] = []

    def second_pass(vertex: Node, component: list[Node]) -> None:
        visited.add(vertex)
        component.append(vertex)
        for neighbor in reversed_adjacency[vertex]:
            if neighbor not in visited:
                second_pass(neighbor, component)

    for vertex in reversed(finish_order):
        if vertex not in visited:
            component: list[Node] = []
            second_pass(vertex, component)
            components.append(tuple(sorted(component)))
    return tuple(components)


def reachable_nodes(graph: Mapping[Node, Sequence[Node]], start: Node) -> frozenset[Node]:
    adjacency = normalize_adjacency_list(graph)
    queue: deque[Node] = deque([start])
    seen = {start}
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return frozenset(seen)


def find_champions(graph: Mapping[Node, Sequence[Node]]) -> tuple[Node, ...]:
    adjacency = normalize_adjacency_list(graph)
    return tuple(
        vertex
        for vertex in adjacency
        if len(reachable_nodes(adjacency, vertex)) == len(adjacency)
    )


def degree_count(edges: Iterable[WeightedEdge]) -> dict[Node, int]:
    counts: defaultdict[Node, int] = defaultdict(int)
    for left, right, _ in edges:
        counts[left] += 1
        counts[right] += 1
    return dict(counts)


def kruskal_mst(vertices: Sequence[Node], edges: Sequence[WeightedEdge]) -> SpanningTreeResult:
    union_find = UnionFind(vertices)
    chosen_edges: list[WeightedEdge] = []
    for edge in sorted(edges, key=lambda item: (item[2], item[0], item[1])):
        left, right, _ = edge
        if union_find.union(left, right):
            chosen_edges.append(edge)
        if len(chosen_edges) == len(vertices) - 1:
            break
    if len(chosen_edges) != len(vertices) - 1:
        raise ValueError("graph is not connected")
    return SpanningTreeResult(
        cost=sum(weight for _, _, weight in chosen_edges),
        edges=tuple(chosen_edges),
        degree_by_vertex=degree_count(chosen_edges),
    )


def exact_degree_constrained_spanning_tree(
    vertices: Sequence[Node],
    edges: Sequence[WeightedEdge],
    degree_limits: Mapping[Node, int],
) -> SpanningTreeResult:
    best_result: SpanningTreeResult | None = None
    for edge_subset in combinations(edges, len(vertices) - 1):
        union_find = UnionFind(vertices)
        valid_tree = True
        for left, right, _ in edge_subset:
            if not union_find.union(left, right):
                valid_tree = False
                break
        if not valid_tree:
            continue
        root = union_find.find(vertices[0])
        if any(union_find.find(vertex) != root for vertex in vertices):
            continue
        degrees = degree_count(edge_subset)
        if any(degrees.get(vertex, 0) > limit for vertex, limit in degree_limits.items()):
            continue
        result = SpanningTreeResult(
            cost=sum(weight for _, _, weight in edge_subset),
            edges=tuple(edge_subset),
            degree_by_vertex=degrees,
        )
        if best_result is None or result.cost < best_result.cost:
            best_result = result
    if best_result is None:
        raise ValueError("no feasible spanning tree satisfies the degree limits")
    return best_result


def degree_constrained_kruskal(
    vertices: Sequence[Node],
    edges: Sequence[WeightedEdge],
    degree_limits: Mapping[Node, int],
) -> SpanningTreeResult:
    union_find = UnionFind(vertices)
    chosen_edges: list[WeightedEdge] = []
    degrees: defaultdict[Node, int] = defaultdict(int)
    for edge in sorted(edges, key=lambda item: (item[2], item[0], item[1])):
        left, right, _ = edge
        if degrees[left] >= degree_limits.get(left, len(vertices)):
            continue
        if degrees[right] >= degree_limits.get(right, len(vertices)):
            continue
        if union_find.union(left, right):
            chosen_edges.append(edge)
            degrees[left] += 1
            degrees[right] += 1
        if len(chosen_edges) == len(vertices) - 1:
            break
    if len(chosen_edges) != len(vertices) - 1:
        raise ValueError("heuristic could not build a spanning tree")
    return SpanningTreeResult(
        cost=sum(weight for _, _, weight in chosen_edges),
        edges=tuple(chosen_edges),
        degree_by_vertex=dict(degrees),
    )


def swap_edge_weights(edges: Sequence[WeightedEdge], first_index: int, second_index: int) -> tuple[WeightedEdge, ...]:
    swapped = list(edges)
    left_start, left_end, left_weight = swapped[first_index]
    right_start, right_end, right_weight = swapped[second_index]
    swapped[first_index] = (left_start, left_end, right_weight)
    swapped[second_index] = (right_start, right_end, left_weight)
    return tuple(swapped)


def best_single_weight_swap(
    vertices: Sequence[Node],
    edges: Sequence[WeightedEdge],
) -> tuple[int, tuple[WeightedEdge, WeightedEdge], SpanningTreeResult]:
    best_cost: int | None = None
    best_pair: tuple[WeightedEdge, WeightedEdge] | None = None
    best_tree: SpanningTreeResult | None = None
    for first_index, second_index in combinations(range(len(edges)), 2):
        swapped_edges = swap_edge_weights(edges, first_index, second_index)
        candidate_tree = kruskal_mst(vertices, swapped_edges)
        if best_cost is None or candidate_tree.cost < best_cost:
            best_cost = candidate_tree.cost
            best_pair = (edges[first_index], edges[second_index])
            best_tree = candidate_tree
    if best_cost is None or best_pair is None or best_tree is None:
        raise ValueError("expected at least one edge pair")
    return best_cost, best_pair, best_tree


def example_single_weight_swap(
    vertices: Sequence[Node],
    edges: Sequence[WeightedEdge],
    first_edge: WeightedEdge,
    second_edge: WeightedEdge,
) -> SpanningTreeResult:
    first_index = edges.index(first_edge)
    second_index = edges.index(second_edge)
    return kruskal_mst(vertices, swap_edge_weights(edges, first_index, second_index))


def dijkstra_shortest_paths(graph: WeightedGraph, start: Node) -> tuple[dict[Node, int], dict[Node, Node | None]]:
    import heapq

    distance = {vertex: 10**12 for vertex in graph}
    previous: dict[Node, Node | None] = {vertex: None for vertex in graph}
    settled: set[Node] = set()
    distance[start] = 0
    priority_queue: list[tuple[int, Node]] = [(0, start)]

    while priority_queue:
        current_distance, vertex = heapq.heappop(priority_queue)
        if vertex in settled:
            continue
        settled.add(vertex)
        for neighbor, weight in graph[vertex]:
            new_distance = current_distance + weight
            if new_distance < distance[neighbor] and neighbor not in settled:
                distance[neighbor] = new_distance
                previous[neighbor] = vertex
                heapq.heappush(priority_queue, (new_distance, neighbor))
    return distance, previous


def bellman_ford_shortest_paths(
    graph: WeightedGraph,
    start: Node,
) -> tuple[dict[Node, int], dict[Node, Node | None]]:
    distance = {vertex: 10**12 for vertex in graph}
    previous: dict[Node, Node | None] = {vertex: None for vertex in graph}
    distance[start] = 0
    edges = [(source, target, weight) for source, neighbors in graph.items() for target, weight in neighbors]

    for _ in range(len(graph) - 1):
        updated = False
        for source, target, weight in edges:
            if distance[source] == 10**12:
                continue
            new_distance = distance[source] + weight
            if new_distance < distance[target]:
                distance[target] = new_distance
                previous[target] = source
                updated = True
        if not updated:
            break

    for source, target, weight in edges:
        if distance[source] != 10**12 and distance[source] + weight < distance[target]:
            raise ValueError("graph contains a negative cycle")
    return distance, previous


def reconstruct_path(previous: Mapping[Node, Node | None], target: Node) -> tuple[Node, ...]:
    path: list[Node] = []
    current: Node | None = target
    while current is not None:
        path.append(current)
        current = previous[current]
    return tuple(reversed(path))


def has_antiparallel_edges(edges: Sequence[WeightedEdge]) -> bool:
    directed_pairs = {(source, target) for source, target, _ in edges}
    return any((target, source) in directed_pairs for source, target, _ in edges)


def resolve_antiparallel_edges(edges: Sequence[WeightedEdge]) -> tuple[WeightedEdge, ...]:
    edge_lookup = {(source, target): weight for source, target, weight in edges}
    handled_pairs: set[frozenset[Node]] = set()
    transformed: list[WeightedEdge] = []

    for source, target, weight in edges:
        if (target, source) not in edge_lookup:
            transformed.append((source, target, weight))
            continue
        unordered_pair = frozenset({source, target})
        if unordered_pair in handled_pairs:
            continue
        keep_source, keep_target = tuple(sorted((source, target)))
        keep_weight = edge_lookup[(keep_source, keep_target)]
        split_weight = edge_lookup[(keep_target, keep_source)]
        split_node = f"{keep_target}_to_{keep_source}"
        transformed.append((keep_source, keep_target, keep_weight))
        transformed.append((keep_target, split_node, split_weight))
        transformed.append((split_node, keep_source, split_weight))
        handled_pairs.add(unordered_pair)
    return tuple(transformed)


def edmonds_karp(edges: Sequence[WeightedEdge], source: Node, sink: Node) -> MaxFlowResult:
    residual: defaultdict[Node, defaultdict[Node, int]] = defaultdict(lambda: defaultdict(int))
    original_edges: list[WeightedEdge] = []

    for start, end, capacity in edges:
        residual[start][end] += capacity
        residual[end]
        original_edges.append((start, end, capacity))

    flow_value = 0
    steps: list[FlowStep] = []

    while True:
        queue: deque[Node] = deque([source])
        parent: dict[Node, Node | None] = {source: None}
        while queue and sink not in parent:
            vertex = queue.popleft()
            for neighbor in sorted(residual[vertex]):
                if residual[vertex][neighbor] > 0 and neighbor not in parent:
                    parent[neighbor] = vertex
                    queue.append(neighbor)
        if sink not in parent:
            break

        path_edges: list[tuple[Node, Node]] = []
        bottleneck = 10**12
        current = sink
        while parent[current] is not None:
            previous = parent[current]
            path_edges.append((previous, current))
            bottleneck = min(bottleneck, residual[previous][current])
            current = previous
        path_edges.reverse()

        for start, end in path_edges:
            residual[start][end] -= bottleneck
            residual[end][start] += bottleneck

        flow_value += bottleneck
        steps.append(
            FlowStep(
                path=tuple([source] + [end for _, end in path_edges]),
                bottleneck=bottleneck,
                total_flow=flow_value,
            )
        )

    reachable = {source}
    queue = deque([source])
    while queue:
        vertex = queue.popleft()
        for neighbor in sorted(residual[vertex]):
            if residual[vertex][neighbor] > 0 and neighbor not in reachable:
                reachable.add(neighbor)
                queue.append(neighbor)

    cut_edges = tuple(
        edge
        for edge in original_edges
        if edge[0] in reachable and edge[1] not in reachable
    )
    return MaxFlowResult(
        value=flow_value,
        steps=tuple(steps),
        min_cut_source_side=frozenset(reachable),
        min_cut_edges=cut_edges,
    )

