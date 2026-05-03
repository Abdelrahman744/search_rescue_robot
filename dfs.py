# dfs.py
# Depth-First Search — goes as deep as possible using a LIFO Stack.
# NOT optimal — finds a path, but not necessarily the shortest.

from maze import get_neighbors


def dfs(start, goal):
    """Run DFS from start to goal. Returns (path, explored_list)."""
    stack = [(start, [start])]              # LIFO stack: (position, path_so_far)
    visited = {start}
    explored = []

    while stack:
        current, path = stack.pop()         # take from top
        explored.append(current)

        if current == goal:
            return path, explored

        for neighbor in reversed(get_neighbors(current)):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

    return None, explored                   # no path found
