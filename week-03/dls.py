"""Depth-Limited Search (DLS) over an adjacency-list graph.

DLS is recursive DFS that never expands a node at depth == limit. Following
the standard formulation (Russell & Norvig), a run ends in one of three states:

    found    a path to the goal exists within the limit
    cutoff   no path found, but the limit pruned at least one unexplored node,
             so a larger limit could still succeed
    failure  no path found and nothing was pruned: the goal is unreachable

DLS is neither complete nor optimal in general (it is incomplete when the goal
lies deeper than the limit), but it bounds memory to O(b*l) for limit l.
Iterative deepening at the bottom of the file removes the guesswork by retrying
with increasing limits.
"""

from typing import Dict, List, NamedTuple, Optional, Set, Tuple

Graph = Dict[str, List[str]]

FOUND = "found"
CUTOFF = "cutoff"
FAILURE = "failure"


class SearchResult(NamedTuple):
    """Outcome of a search run."""

    status: str                         # FOUND, CUTOFF or FAILURE
    path: Optional[List[str]]           # start..goal inclusive when FOUND, else None
    visited_log: List[Tuple[str, int]]  # (node, depth) in visiting order
    nodes_visited: int                  # len(visited_log)


def get_known_nodes(graph: Graph) -> Set[str]:
    """Return all node names, including those that only appear as neighbours."""
    known = set(graph)
    for neighbours in graph.values():
        known.update(neighbours)
    return known


def validate_depth_limit(depth_limit: int) -> None:
    """Raise ValueError unless ``depth_limit`` is an integer >= 0."""
    # bool is a subclass of int, so True/False would otherwise pass as 1/0.
    if not isinstance(depth_limit, int) or isinstance(depth_limit, bool) or depth_limit < 0:
        raise ValueError("Depth limit must be a non-negative integer.")


def depth_limited_search(graph: Graph, start: str, goal: str, depth_limit: int) -> SearchResult:
    """Search for a path from ``start`` to ``goal`` within ``depth_limit`` edges.

    Recursion depth is bounded by the path length, so graphs whose simple paths
    exceed Python's recursion limit (~1000) would need an iterative rewrite.

    Args:
        graph: Adjacency list mapping each node to its neighbours. A neighbour
            without its own entry is treated as a dead end.
        start: Node to begin from (depth 0).
        goal: Node to reach.
        depth_limit: Deepest level that may be visited; nodes at this depth are
            tested but not expanded.

    Returns:
        A ``SearchResult`` with the status, the path (if found) and a visit log.

    Raises:
        ValueError: If the limit is invalid, or ``start`` / ``goal`` does not
            appear in the graph.
    """
    validate_depth_limit(depth_limit)
    known_nodes = get_known_nodes(graph)
    if start not in known_nodes:
        raise ValueError(f"Start node '{start}' is not in the graph.")
    if goal not in known_nodes:
        raise ValueError(f"Goal node '{goal}' is not in the graph.")

    visited_log: List[Tuple[str, int]] = []
    current_path: List[str] = [start]   # root-to-current path, mutated as we recurse
    nodes_on_path: Set[str] = {start}   # set view of current_path for O(1) cycle checks

    # Shallowest depth at which each node has been explored. Re-entering a node
    # at an equal or greater depth cannot succeed where the earlier visit did
    # not, since it has less remaining depth budget. Pruning these revisits
    # avoids exponential re-exploration without changing the returned status.
    shallowest_depth: Dict[str, int] = {}

    def explore(node: str, depth: int) -> Tuple[str, Optional[List[str]]]:
        """Visit ``node`` at ``depth`` and return ``(status, path)`` for its subtree."""
        visited_log.append((node, depth))
        shallowest_depth[node] = depth

        if node == goal:
            return FOUND, list(current_path)    # copy: current_path is mutated on backtrack

        neighbours = graph.get(node, [])

        if depth == depth_limit:
            # Report CUTOFF only if expansion was actually prevented. If every
            # neighbour is already on the path there was nothing left to explore.
            if any(n not in nodes_on_path for n in neighbours):
                return CUTOFF, None
            return FAILURE, None

        cutoff_occurred = False
        for neighbour in neighbours:
            if neighbour in nodes_on_path:      # would close a cycle
                continue
            if shallowest_depth.get(neighbour, depth_limit + 1) <= depth + 1:
                continue                        # already explored with at least as much budget

            current_path.append(neighbour)
            nodes_on_path.add(neighbour)
            status, path = explore(neighbour, depth + 1)
            current_path.pop()                  # backtrack
            nodes_on_path.remove(neighbour)

            if status == FOUND:
                return FOUND, path
            if status == CUTOFF:
                cutoff_occurred = True          # another branch may still succeed

        # Subtree exhausted: CUTOFF if any descendant was pruned by the limit.
        return (CUTOFF if cutoff_occurred else FAILURE), None

    status, path = explore(start, 0)
    return SearchResult(status, path, visited_log, len(visited_log))


def iterative_deepening_search(
    graph: Graph, start: str, goal: str, max_depth: int
) -> Tuple[SearchResult, int]:
    """Run DLS with limits 0, 1, 2, ... up to ``max_depth``.

    Stops at the first non-CUTOFF result. A FOUND result has the fewest edges,
    because every shallower limit was already exhausted; FAILURE means the goal
    is unreachable, so larger limits cannot help.

    Args:
        graph: Adjacency list of the graph.
        start: Node to begin from.
        goal: Node to reach.
        max_depth: Largest limit to try (>= 0).

    Returns:
        ``(result, limit_used)`` for the last DLS run.

    Raises:
        ValueError: Same conditions as ``depth_limited_search``.
    """
    validate_depth_limit(max_depth)
    for limit in range(max_depth + 1):
        result = depth_limited_search(graph, start, goal, limit)
        if result.status != CUTOFF:
            return result, limit
    return result, max_depth    # still CUTOFF at max_depth


def run_dls(graph: Graph, start: str, goal: str, depth_limit: int) -> None:
    """Run DLS once and print visited nodes with depths, the status and the path."""
    print(f"DLS from '{start}' to '{goal}' with depth limit {depth_limit!r}")
    try:
        result = depth_limited_search(graph, start, goal, depth_limit)
    except ValueError as error:
        print(f"  Error: {error}\n")
        return

    print("  Visited (node@depth): " + ", ".join(f"{n}@{d}" for n, d in result.visited_log))
    print(f"  Status: {result.status}   (nodes visited: {result.nodes_visited})")
    if result.path is not None:
        print(f"  Path: {' -> '.join(result.path)}  (edges: {len(result.path) - 1})")
    elif result.status == CUTOFF:
        print("  No path within the limit; a larger limit might find one.")
    else:
        print("  Goal is unreachable from the start node.")
    print()


def run_iterative_deepening(graph: Graph, start: str, goal: str, max_depth: int) -> None:
    """Run iterative deepening once and print the limit at which it stopped."""
    print(f"Iterative deepening from '{start}' to '{goal}' (max depth {max_depth})")
    try:
        result, limit = iterative_deepening_search(graph, start, goal, max_depth)
    except ValueError as error:
        print(f"  Error: {error}\n")
        return
    print(f"  Stopped at limit {limit} with status: {result.status}")
    if result.path is not None:
        print(f"  Path: {' -> '.join(result.path)}  (edges: {len(result.path) - 1})")
    print()


def run_self_tests() -> None:
    """Assertion-based checks covering all three statuses, limit 0 and invalid input."""
    # Direct edge S-G (1 edge) versus S-A-B-G (3 edges).
    graph = {"S": ["A", "G"], "A": ["S", "B"], "B": ["A", "S", "G"], "G": ["B", "S"]}
    assert depth_limited_search(graph, "S", "G", 1).path == ["S", "G"]
    assert depth_limited_search(graph, "S", "G", 0).status == CUTOFF

    # Linear chain: the goal sits exactly 3 edges from the start.
    chain = {"A": ["B"], "B": ["A", "C"], "C": ["B", "D"], "D": ["C"]}
    assert depth_limited_search(chain, "A", "D", 3).status == FOUND
    assert depth_limited_search(chain, "A", "D", 2).status == CUTOFF

    # Limit 0 only permits testing the start node itself.
    assert depth_limited_search(chain, "A", "A", 0).path == ["A"]
    assert depth_limited_search(chain, "A", "B", 0).status == CUTOFF

    # Unreachable goal in a graph with a cycle: FAILURE, not CUTOFF.
    cyclic = {"X": ["Y"], "Y": ["Z"], "Z": ["X"], "W": []}
    assert depth_limited_search(cyclic, "X", "W", 10).status == FAILURE

    # Neighbour with no adjacency entry is a dead end.
    assert depth_limited_search({"A": ["B"]}, "A", "B", 1).path == ["A", "B"]

    # Invalid limits and unknown nodes must be rejected.
    invalid_calls = [
        (graph, "S", "G", -1),      # negative
        (graph, "S", "G", 2.5),     # non-integer
        (graph, "S", "G", True),    # bool masquerading as int
        (graph, "Q", "G", 1),       # unknown start
        (graph, "S", "Q", 1),       # unknown goal
    ]
    for args in invalid_calls:
        try:
            depth_limited_search(*args)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {args[1:]}")

    # Iterative deepening returns the shallowest solution.
    result, limit = iterative_deepening_search(graph, "S", "G", 5)
    assert result.path == ["S", "G"] and limit == 1
    assert iterative_deepening_search(cyclic, "X", "W", 5)[0].status == FAILURE

    print("DLS self-tests passed.")


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

    run_dls(sample_graph, "A", "G", 3)    # goal exactly at the limit -> found
    run_dls(sample_graph, "A", "G", 2)    # limit too small -> cutoff
    run_dls(sample_graph, "A", "G", 10)   # generous limit -> found
    run_dls(sample_graph, "A", "A", 0)    # limit 0, start == goal -> found
    run_dls(sample_graph, "A", "G", 0)    # limit 0, goal elsewhere -> cutoff
    run_dls(sample_graph, "A", "H", 10)   # unreachable -> failure
    run_dls(sample_graph, "A", "Z", 3)    # unknown goal
    run_dls(sample_graph, "A", "G", -1)   # invalid limit (negative)
    run_dls(sample_graph, "A", "G", 2.5)  # invalid limit (non-integer)

    run_iterative_deepening(sample_graph, "A", "G", 6)   # stops at limit 3

    run_self_tests()
