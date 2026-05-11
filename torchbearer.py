"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: ___________________________
Student ID:   ___________________________

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    TODO
    """
    return """
    Why a single shortest-path run from S is not enough:
    A single shortest-path run from S to T is not enough because a shortest-path run does not necessarily guarantee that traversal through all relics.
    Furthermore, when going from S to relic R1, shortest path only provides a path starting from S and therefore once at R1, we don't know the path to 
    the next relic.

    What decision remains after all inter-location costs are known:
    After all inter-location costs are known, the optimal order I traverse through all relics still remain.

    Why this requires a search over orders (one sentence):
    This requires a search over orders because local decisions don't guarantee a global optimum
    """


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    TODO
    """

    # We want paths from spawn and relics
    # No need to add exit_node because at no point will we travel FROM exit_node
    # Use set because no duplicates and order does not matter
    sources = set()
    sources.add(spawn)

    for r in relics:
        sources.add(r)

    return list(sources)


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    TODO
    """
    dist = {node: float('inf') for node in graph}
    dist[source] = 0

    heap = [(0, source)]
    visited = set()

    while heap:
        _, u = heapq.heappop(heap)

        if u in visited:
            continue
        visited.add(u)

        # Relaxation check for all neighbors
        for v, cost_v in graph[u]:
            new_cost = dist[u] + cost_v
            if new_cost < dist[v]:
                dist[v] = new_cost
                heapq.heappush(heap, (new_cost, v))

    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    TODO
    """
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {}
    for src in sources:
        dist_table[src] = run_dijkstra(graph, src)
    return dist_table



# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    TODO
    """
    return """
    ## Part 3: Algorithm Correctness

    > Document your understanding of why Dijkstra produces correct distances.
    > Bullet points and short sentences throughout. No paragraphs.

    ### Part 3a: What the Invariant Means

    - **For nodes already finalized (in S):**
    distance for a given node is the guaranteed shortest path from the source

    - **For nodes not yet finalized (not in S):**
    distance for a given node is the shortest path discovered so far from the source traveling through finalized nodes 

    ### Part 3b: Why Each Phase Holds

    - **Initialization : why the invariant holds before iteration 1:**
    - The source node's distance is set to 0 as the node's distance to itself is naturally 0
    - All other nodes are not finalized nor discovered and therefore invariant holds

    - **Maintenance : why finalizing the min-dist node is always correct:**
    - Given nonnegative edge weights (no future paths can reduce cost), any other path would require going through another unfinalized node v which costs greater than or equal to the min-dist node.

    - **Termination : what the invariant guarantees when the algorithm ends:**
    - All reachable nodes have been finalized and therefore distance for all nodes are the guaranteed shortest path from the source.

    ### Part 3c: Why This Matters for the Route Planner

    > One sentence connecting correct distances to correct routing decisions.

    If distances are incorrect, route costs may be incorrectly calculated and the returned route may not be the optimal route.
    """


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    TODO
    """
    return """
    ## Part 4: Search Design

    ### Why Greedy Fails

    - **The failure mode:** _Greedy selecting the cheapest discovered edge to an unvisited neighbor which may lead to less than optimal total costs._
    - **Counter-example setup:** 

    | From / To | A   | B   | C   | T   |
    | --------- | --- | --- | --- | --- |
    | S         | 20  | 10  | 20  | -   |
    | A         | -   | 50  | 10  | 10  |
    | B         | 10  | -   | 50  | 100 |
    | C         | 10  | 10  | -   | 100 |

    - **What greedy picks:** _S->B->A->C->T = 10+10+10+100 = 130_
    - **What optimal picks:** _S->B->C->A->T = 10+50+10+10 = 80_
    - **Why greedy loses:** _Greedy loses due to failing to account for future better paths_

    ### What the Algorithm Must Explore

    - _The algorithm must explore all possible orders of visiting the relics to find which provides the shortest path to T from S_
    """


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    pass


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    pass


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    pass


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
