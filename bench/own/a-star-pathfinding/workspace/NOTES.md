# Notes

## What Jordan knows
- Python from classes, and a small 2D grid game in Pygame with a player who moves tile by tile.
- A grid as a graph: each tile is a node, and its neighbors are the tiles one step away (learning record 0001).
- Breadth-first search from a data structures course: it explores tiles in the order they were discovered, using a queue, and finds the path with the fewest steps when every step costs the same (learning record 0001).
- A*'s three values at the level of definitions: g is the cost so far, h is the estimate of what is left, and f is their sum (learning record 0002).

## What Jordan does not know yet
- How A* chooses which tile to expand next, what the open set and closed set hold, and when the search stops.
- How a tile's values change when a cheaper path to it is found, and how the final path is rebuilt.
- What makes a heuristic admissible, and how the choice of heuristic affects speed and whether the path is the shortest.

## Working notes
- Quiz 0001 (g, h and f) was taken right after the session on g, h and f, in `submissions/s1.json`; it has not been graded yet.
- Next in the mission is how A* runs: the open set, the closed set and node expansion, because the guards need a working search before the heuristic can be tuned.
