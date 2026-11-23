# A* scores each tile with g, h and f

Jordan can state A*'s three values: g(n) is the cost of the path so far from the start to tile n, h(n) is an estimate of the cost from n to the goal, and f(n) = g(n) + h(n).
These values are what A* uses to decide where to search next, so every later session on how A* runs builds on them.

**Evidence:** Gave the three definitions in their own words and added g and h for one tile in a small example.

**Implications:** Not yet checked: whether Jordan sees that g counts the detours of the path actually found, not the distance from the start, and that h is only an estimate.
Quiz 0001 tests both, along with Manhattan distance and diagonal step costs.
Next in the mission is the open set, the closed set and node expansion.
