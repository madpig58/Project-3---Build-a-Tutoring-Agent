# A grid map is a graph, and breadth-first search finds the fewest-step path on it

Jordan disclosed that they already know breadth-first search from a data structures course and can treat a game's grid map as a graph, with each tile a node and its neighbors the tiles one step away.
This is the floor for A*: later sessions can build on neighbors and a list of tiles to visit without re-teaching them.

**Evidence:** Described how breadth-first search uses a queue to explore tiles in the order they were discovered, and why it finds the path with the fewest steps when every step costs the same.

**Implications:** Jordan has not yet met searches where steps cost different amounts, or a search that uses an estimate of the distance left.
