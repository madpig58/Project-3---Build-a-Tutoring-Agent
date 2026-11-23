# Mission: A* pathfinding for game NPCs

## Why
I am building a small top-down 2D game in Python with Pygame, and the guard NPCs need to chase the player around walls instead of walking straight into them.
I want to write A* myself rather than copy a library, so I need to understand it well enough to trace it by hand, debug it when a guard takes a strange route, and defend my choice of heuristic.

## Success looks like
- I can work out g, h and f for any tile in a small grid example.
- I can trace A* step by step on paper: which tile it expands next, what goes in the open and closed sets, and when it stops.
- I can implement A* for my guards on a grid map and rebuild the path they should follow.
- I can choose a heuristic for 4-direction and 8-direction movement and explain how it affects speed and whether the path is the shortest.

## Constraints
- I have a few hours a week alongside my courses.
- I am comfortable with Python and breadth-first search, but I have not implemented A* before.
- The game runs at 60 frames per second, so a search must not take too long when several guards replan.

## Out of scope
- Navigation meshes and 3D pathfinding.
- Steering, animation and crowd movement.
- Machine-learning approaches to pathfinding.
