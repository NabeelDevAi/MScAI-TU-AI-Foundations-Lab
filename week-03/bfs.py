"""Breadth-First Search (BFS) over an adjacency-list graph.

Nodes are expanded in order of increasing distance from the start, using a FIFO
queue. On an unweighted graph the first path found to the goal therefore has the
minimum number of edges (BFS is complete and optimal for unit step costs).

Complexity, with b = branching factor and d = depth of the shallowest goal:
    time  O(b^d)   (O(V + E) in the worst case on a finite graph)
    space O(b^d)   (the frontier is held in memory)
"""

from collections import deque
from typing import Deque, Dict, List, NamedTuple, Optional, Set

Graph = Dict[str, List[str]]


class SearchResult(NamedTuple):
    """Outcome of a search run, including basic cost metrics."""

    path: Optional[List[str]]   # start..goal inclusive; None when the goal is unreachable
    traversal_order: List[str]  # nodes in the order they were visited
    nodes_expanded: int         # nodes whose neighbours were generated
    max_queue_size: int         # peak frontier size, a proxy for memory use


def get_known_nodes(graph: Graph) -> Set[str]:
    """Return all node names, including those that only appear as neighbours."""
    known = set(graph)
    for neighbours in graph.values():
        known.update(neighbours)
    return known


def rebuild_path(parents: Dict[str, Optional[str]], goal: str) -> List[str]:
    """Reconstruct the start-to-goal path by following parent links backwards.

    Args:
        parents: Maps each discovered node to its predecessor (None for the start).
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


def breadth_first_search(graph: Graph, start: str, goal: str) -> SearchResult:
    """Find a minimum-edge path from ``start`` to ``goal``.

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

    if start == goal:
        return SearchResult([start], [start], 0, 1)

    # `parents` is both the predecessor map and the visited set. Nodes are
    # marked on discovery rather than on dequeue, so each is enqueued at most once.
    parents: Dict[str, Optional[str]] = {start: None}
    frontier: Deque[str] = deque([start])
    traversal_order: List[str] = []
    nodes_expanded = 0
    max_queue_size = 1

    while frontier:
        current = frontier.popleft()
        traversal_order.append(current)
        nodes_expanded += 1

        for neighbour in graph.get(current, []):
            if neighbour in parents:
                continue
            parents[neighbour] = current

            # Goal test at generation time. With unit costs the first discovery
            # of the goal is already optimal, so this saves expanding the rest
            # of the current level.
            if neighbour == goal:
                traversal_order.append(neighbour)
                return SearchResult(
                    rebuild_path(parents, goal), traversal_order, nodes_expanded, max_queue_size
                )

            frontier.append(neighbour)
            max_queue_size = max(max_queue_size, len(frontier))

    # Frontier exhausted without discovering the goal.
    return SearchResult(None, traversal_order, nodes_expanded, max_queue_size)


def run_bfs(graph: Graph, start: str, goal: str) -> None:
    """Run BFS for one start/goal pair and print the traversal, path and metrics."""
    print(f"BFS from '{start}' to '{goal}'")
    try:
        result = breadth_first_search(graph, start, goal)
    except ValueError as error:
        print(f"  Error: {error}\n")
        return

    print(f"  Traversal order: {' -> '.join(result.traversal_order)}")
    if result.path is None:
        print("  Result: goal is unreachable from the start node.")
    else:
        print(f"  Path: {' -> '.join(result.path)}  (edges: {len(result.path) - 1})")
    print(f"  Stats: expanded={result.nodes_expanded}, max queue size={result.max_queue_size}\n")


def run_self_tests() -> None:
    """Assertion-based checks covering optimality, cycles and invalid input."""
    # Two routes S->G: a direct edge and S-A-B-G. BFS must return the direct one.
    graph = {"S": ["A", "G"], "A": ["S", "B"], "B": ["A", "S", "G"], "G": ["B", "S"]}
    assert breadth_first_search(graph, "S", "G").path == ["S", "G"]

    # Cycle X -> Y -> Z -> X must terminate; W is a disconnected node.
    cyclic = {"X": ["Y"], "Y": ["Z"], "Z": ["X"], "W": []}
    assert breadth_first_search(cyclic, "X", "Z").path == ["X", "Y", "Z"]
    assert breadth_first_search(cyclic, "X", "W").path is None

    # Degenerate cases: start == goal, and a neighbour with no adjacency entry.
    assert breadth_first_search(graph, "A", "A").path == ["A"]
    assert breadth_first_search({"A": ["B"]}, "A", "B").path == ["A", "B"]

    # Unknown start or goal must be rejected.
    for bad_start, bad_goal in (("Q", "S"), ("S", "Q")):
        try:
            breadth_first_search(graph, bad_start, bad_goal)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for an unknown node")

    print("BFS self-tests passed.")


if __name__ == "__main__":
    # Undirected sample graph (each edge listed in both directions). It contains
    # cycles, and H-I is a separate component to exercise the unreachable case.
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

    run_bfs(sample_graph, "A", "G")   # reachable; optimal path is 3 edges
    run_bfs(sample_graph, "A", "A")   # start == goal
    run_bfs(sample_graph, "A", "H")   # different component
    run_bfs(sample_graph, "A", "Z")   # unknown goal
    run_bfs(sample_graph, "Q", "A")   # unknown start

    run_self_tests()
