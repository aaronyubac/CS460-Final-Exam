# The Torchbearer

**Student Name:** ___________________________
**Student ID:** ___________________________
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  A single shortest-path run from S to T is not enough because a shortest-path run does not necessarily guarantee that traversal through all relics. Furthermore, when going from S to relic R1, shortest path only provides a path starting from S and therefore once at R1, we don't know the path to the next relic.

- **What decision remains after all inter-location costs are known:**
  After all inter-location costs are known, the optimal order I traverse through all relics still remain.

- **Why this requires a search over orders (one sentence):**
  This requires a search over orders because local decisions don't guarantee a global optimum.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source                                  |
| ---------------- | --------------------------------------------------- |
| _Spawn_          | _We start from S and need a path from S to a relic_ |
| _Relics_         | _We need a path from each relic to the next_        |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property                    | Your answer                 |
| --------------------------- | --------------------------- |
| Data structure name         | Nested Dictionary           |
| What the keys represent     | Source and Destination Node |
| What the values represent   | Distance from u to v        |
| Lookup time complexity      | O(1)                        |
| Why O(1) lookup is possible | Hashing                     |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** _k+1_
- **Cost per run:** _O(mlog(n))
- **Total complexity:** _O(kmlog(n))_
- **Justification (one line):** _Given that Dijkstras is ran k+1 times (k relics + S), and Dijkstras has a time complexity of O(mlog(n)), the total complexity comes out to O(kmlog(n))_

---

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

---

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

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component                | Variable name in code | Data type   | Description                                |
| ------------------------ | --------------------- | ----------- | ------------------------------------------ |
| Current location         | curr_location         | node        | Torchbearer's current location             |
| Relics already collected | visited               | set\[node\] | Set of relics already collected            |
| Fuel cost so far         | total_cost            | int         | Total fuel spent to reach current location |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property                                    | Your answer                                                                                                            |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Data structure chosen                       | Set                                                                                                                    |
| Operation: check if relic already collected | Time complexity: O(1)                                                                                                  |
| Operation: mark a relic as collected        | Time complexity: O(1)                                                                                                  |
| Operation: unmark a relic (backtrack)       | Time complexity: O(1)                                                                                                  |
| Why this structure fits                     | Order doesn't matter and allows for quick checks and adding nodes making it good for tracking visited relics sites for |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** _k!_
- **Why:** _When you start you have k choices, then from there you have k-1 choices, then k-2 and so on._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** _current best total cost and path taken_
- **When it is used:** _when comparing with the current total cost and updating path_
- **What it allows the algorithm to skip:** _when the current total cost exceeds the best so far, the algorithm skips remaining orderings of that branch_

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** _current cost, current location, and relics unvisited_
- **What the lower bound accounts for:** _current cost + for all unvisited relics, sum(min(dist_table\[curr\]\[relic\]) + dist_table\[relic\]\[exit\]_
- **Why it never overestimates:** _Dijkstra's is guaranteed optimal, so summing the cheapest cost to each unvisited relic and exit can never overestimate the remaining cost_

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- Lower bound never overestimates and therefore, current cost + the lower bound is the guaranteed lowest cost to complete the branch
- If the sum of current cost + the lower bound is greater than or equal to the current best, then there are no ways for the cost to improve (unless negative)

---

## References

- _Lecture Notes_
