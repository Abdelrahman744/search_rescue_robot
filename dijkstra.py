# dijkstra.py
# Dijkstra's Algorithm — explores by lowest cumulative cost using a Priority Queue.
# ALWAYS optimal for non-negative edge weights.

import heapq
from maze import get_neighbors, get_cost, reconstruct_path


def dijkstra(start, goal):
    """Run Dijkstra from start to goal. Returns (path, explored_list, total_cost)."""
    pq = [(0, start)]                       # min-heap: (cost, position)
    cost_so_far = {start: 0}
    came_from = {start: None}
    explored = []

    while pq:
        current_cost, current = heapq.heappop(pq)
        explored.append(current)

        # Skip stale entries
        if current_cost > cost_so_far.get(current, float('inf')):
            continue

        if current == goal:
            return reconstruct_path(came_from, start, goal), explored, current_cost

        for neighbor in get_neighbors(current):
            new_cost = current_cost + get_cost(neighbor)
            if new_cost < cost_so_far.get(neighbor, float('inf')):
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    return None, explored, float('inf')     # no path found
