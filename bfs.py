# bfs.py
# Breadth-First Search — explores level by level using a FIFO Queue.
# Optimal for unweighted graphs (fewest hops), NOT cost-optimal.

from collections import deque
from maze import get_neighbors, reconstruct_path


def bfs(start, goal):
    """Run BFS from start to goal. Returns (path, explored_list)."""
    frontier = deque([start])               # FIFO queue
    came_from = {start: None}               # tracks parent of each visited cell
    explored = []

    while frontier:
        current = frontier.popleft()        # take from front
        explored.append(current)

        if current == goal:
            return reconstruct_path(came_from, start, goal), explored

        for neighbor in get_neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                frontier.append(neighbor)

    return None, explored                   # no path found
