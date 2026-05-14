# Development Log – The Torchbearer

**Student Name:** Aaron Anthony Yubac
**Student ID:** 131379284

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – 5/7: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

I plan on initially implementing core functions which drive our algorithm; this includes `select_sources`, `run_dijkstra` and `precompute_distances`. I expect building an understanding of how all parts work together to cause some difficulty as well as implementation for parts of functions like backtracking to be difficult. As for testing, I plan on understanding and utilizing the provided \_run_tests() function to test for overall behavior. I also plan to test certain parts by themself to ensure their functionality works in isolation such as making sure that Dijkstra's is returning the expected values.

---

## Entry 2 – 5/9: run_dijkstra() implementation

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

Initially, I didn't fully understand the heapq library so during implementation of run_dijkstra(), after reviewing how the algorithm worked I just started implementation based on the different working parts of the algorithm. This meant keeping a min heap which kept track of nodes and the cost to reach them. I however didn't have a use for the cost in terms of accessing and was unsure if I should keep it since it wasn't being accessed. However I knew that those weights needed to be used in order to sort within the min heap and after a little research I discovered that heapq sorts tuples based on the first element and uses following elements as tie-breakers. So I kept the cost and when accessing the heap instead of declaring variables for both cost, node I ended up using a blank identifier, `_, node` in order to maintain the cost for sorting while not keeping an unused variable.

---

## Entry 3 – \[5/14\]: \[\_explore()\]

Something I had trouble building and understanding the logic of initially was the pruning. Once I understood the conditions and logic behind it, I was able to build out a foundation for it. I however had a hole in logic for my initial implementation. Because the way I understood the lower bound to be the sum of the minimums to each node I ended up writing `sum(min())` when gathering the sums of the `dist_table`. This is however wrong because min just returns a single value and I wanted the sum of all those min. I failed to realize that the `dist_table` already provides that minimum distance to a given node and instead I just need `sum()` for all relics remaining without `min()`.

---

## Entry 4 – \[5/14\]: Post-Implementation Reflection

While I wouldn't change much and I actually really enjoyed this approach to programming I would however probably build stronger input validation as well as make it more accessible for use by average users maybe via GUI. I also would have provided more documentation so that when I come back to it I have a full idea of what's going on. Overall I thought it was a great experience to go through programming while having that approach of fully grasping the problem and coming up with stronger solutions.

---

## Final Entry – \[5/14\]: Time Estimate

| Part                           | Estimated Hours  |
| ------------------------------ | ---------------- |
| Part 1: Problem Analysis       | 1                |
| Part 2: Precomputation Design  | 2                |
| Part 3: Algorithm Correctness  | 1                |
| Part 4: Search Design          | .5               |
| Part 5: State and Search Space | 1                |
| Part 6: Pruning                | 2                |
| Part 7: Implementation         | Included by part |
| README and DEVLOG writing      | 5                |
| **Total**                      | 12.5             |
