# maze.py
# Defines the maze layout, constants, and shared helper functions.

# Cell values:
#   0 → Clear path     (traversal cost = 1)
#   1 → Wall / debris  (impassable)
#   5 → Hazardous area (traversal cost = 5)

MAZE = [
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 1, 5],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 5],
    [1, 1, 0, 1, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 0, 0, 0],
]

START = (0, 0)   # Robot's initial position (top-left)
GOAL  = (9, 9)   # Survivor's location (bottom-right)

ROWS = len(MAZE)
COLS = len(MAZE[0])

# Four cardinal directions: Up, Down, Left, Right
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def get_neighbors(pos):
    """Return all valid (in-bounds, non-wall) neighbors of pos."""
    r, c = pos
    neighbors = []
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] != 1:
            neighbors.append((nr, nc))
    return neighbors


def get_cost(pos):
    """Return traversal cost: hazardous (5) → 5, clear (0) → 1."""
    r, c = pos
    value = MAZE[r][c]
    return value if value > 0 else 1


def reconstruct_path(came_from, start, goal):
    """Trace back from goal to start using came_from dict."""
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path
