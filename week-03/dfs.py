"""Depth-First Search (DFS) over an adjacency-list graph.

Implemented iteratively with an explicit LIFO stack, which avoids Python's
recursion limit on deep graphs. DFS is complete on finite graphs once visited
nodes are tracked, but it is not optimal: the path returned depends on
neighbour ordering and may be far longer than the shortest one.

Complexity, with b = branching factor and m = maximum depth:
    time  O(b^m)   (O(V + E) with a visited set)
    space O(b*m) for a tree; with the pending-entry stack used here, O(E) worst case
"""

from typing import Dict, List, NamedTuple, Optional, Set, Tuple

Graph = Dict[str, List[str]]


class SearchResult(NamedTuple):
    """Outcome of a search run, including basic cost metrics."""

    path: Optional[List[str]]   # start..goal inclusive; None when the goal is unreachable
    traversal_order: List[str]  # nodes in the order they were visited
    nodes_expanded: int         # nodes whose neighbours were generated
    max_stack_size: int         # peak stack size, a proxy for memory use


def get_known_nodes(graph: Graph) -> Set[str]:
    """Return all node names, including those that only appear as neighbours."""
    known = set(graph)
    for neighbours in graph.values():
        known.update(neighbours)
    return known


def rebuild_path(parents: Dict[str, Optional[str]], goal: str) -> List[str]:
    """Reconstruct the start-to-goal path by following parent links backwards.

    Args:
        parents: Maps each visited node to the node it was reached from
            (None for the start).
        goal: Node to trace back from.

    Returns:
        Nodes from the start to ``goal`` inclusive.
    """
    path: List[str] = []
    node: Optional[str] = goal
    while node is not None:
        path.append(node)
        node = parents[node]
    path.reverse()
    return path


def depth_first_search(graph: Graph, start: str, goal: str) -> SearchResult:
    """Find a path from ``start`` to ``goal`` (not necessarily the shortest).

    Args:
        graph: Adjacency list mapping each node to its neighbours. A neighbour
            without its own entry is treated as a dead end.
        start: Node to begin from.
        goal: Node to reach.

    Returns:
        A ``SearchResult``; ``path`` is None if the goal is unreachable.

    Raises:
        ValueError: If ``start`` or ``goal`` does not appear in the graph.
    """
    known_nodes = get_known_nodes(graph)
    if start not in known_nodes:
        raise ValueError(f"Start node '{start}' is not in the graph.")
    if goal not in known_nodes:
        raise ValueError(f"Goal node '{goal}' is not in the graph.")

    # Stack entries are (node, predecessor). The predecessor is bound at push
    # time but only recorded once the entry is popped, so `parents` always
    # reflects the edge that was actually followed.
    stack: List[Tuple[str, Optional[str]]] = [(start, None)]
    parents: Dict[str, Optional[str]] = {}      # doubles as the visited set
    traversal_order: List[str] = []
    nodes_expanded = 0
    max_stack_size = 1

    while stack:
        current, predecessor = stack.pop()

        # A node may be pushed several times before its first pop. Skipping
        # already-visited entries is what guarantees termination on cyclic graphs.
        if current in parents:
            continue
        parents[current] = predecessor
        traversal_order.append(current)
        nodes_expanded += 1

        if current == goal:
            return SearchResult(
                rebuild_path(parents, goal), traversal_order, nodes_expanded, max_stack_size
            )

        # Push in reverse so the first-listed neighbour is popped, and so
        # explored, first. This keeps the traversal order deterministic and
        # identical to the usual recursive formulation.
        for neighbour in reversed(graph.get(current, [])):
            if neighbour not in parents:
                stack.append((neighbour, current))
        max_stack_size = max(max_stack_size, len(stack))

    # Stack exhausted without reaching the goal.
    return SearchResult(None, traversal_order, nodes_expanded, max_stack_size)


def run_dfs(graph: Graph, start: str, goal: str) -> None:
    """Run DFS for one start/goal pair and print the traversal, path and metrics."""
    print(f"DFS from '{start}' to '{goal}'")
    try:
        result = depth_first_search(graph, start, goal)
    except ValueError as error:
        print(f"  Error: {error}\n")
        return

    print(f"  Traversal order: {' -> '.join(result.traversal_order)}")
    if result.path is None:
        print("  Result: goal is unreachable from the start node.")
    else:
        print(f"  Path: {' -> '.join(result.path)}  (edges: {len(result.path) - 1})")
    print(f"  Stats: expanded={result.nodes_expanded}, max stack size={result.max_stack_size}\n")


def run_self_tests() -> None:
    """Assertion-based checks covering validity, non-optimality, cycles and invalid input."""
    # S->G is a direct edge, but DFS commits to S->A first and returns the
    # longer S-A-B-G. Valid, yet not shortest: this is the expected behaviour.
    graph = {"S": ["A", "G"], "A": ["S", "B"], "B": ["A", "S", "G"], "G": ["B", "S"]}
    assert depth_first_search(graph, "S", "G").path == ["S", "A", "B", "G"]

    # Cycle X -> Y -> Z -> X must terminate; W is a disconnected node.
    cyclic = {"X": ["Y"], "Y": ["Z"], "Z": ["X"], "W": []}
    assert depth_first_search(cyclic, "X", "Z").path == ["X", "Y", "Z"]
    assert depth_first_search(cyclic, "X", "W").path is None

    # Degenerate cases: start == goal, and a neighbour with no adjacency entry.
    assert depth_first_search(graph, "A", "A").path == ["A"]
    assert depth_first_search({"A": ["B"]}, "A", "B").path == ["A", "B"]

    # Every consecutive pair in the returned path must be a real edge.
    path = depth_first_search(graph, "S", "G").path
    assert all(b in graph[a] for a, b in zip(path, path[1:]))

    # Unknown start or goal must be rejected.
    for bad_start, bad_goal in (("Q", "S"), ("S", "Q")):
        try:
            depth_first_search(graph, bad_start, bad_goal)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for an unknown node")

    print("DFS self-tests passed.")


if __name__ == "__main__":
    # Same undirected sample graph as bfs.py: cyclic, with H-I as a separate component.
    sample_graph: Graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B", "G"],
        "E": ["B", "F"],
        "F": ["C", "E", "G"],
        "G": ["D", "F"],
        "H": ["I"],
        "I": ["H"],
    }

    run_dfs(sample_graph, "A", "G")   # valid path; shortest not guaranteed
    run_dfs(sample_graph, "A", "A")   # start == goal
    run_dfs(sample_graph, "A", "H")   # different component
    run_dfs(sample_graph, "A", "Z")   # unknown goal
    run_dfs(sample_graph, "Q", "A")   # unknown start

    run_self_tests()
