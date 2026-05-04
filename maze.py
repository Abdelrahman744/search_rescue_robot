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


def get_neighbors(position):
    """Return all valid (in-bounds, non-wall) neighbors of position."""
    row, col = position
    neighbors = []
    for delta_row, delta_col in DIRECTIONS:
        neighbor_row, neighbor_col = row + delta_row, col + delta_col
        if 0 <= neighbor_row < ROWS and 0 <= neighbor_col < COLS and MAZE[neighbor_row][neighbor_col] != 1:
            neighbors.append((neighbor_row, neighbor_col))
    return neighbors


def get_cost(position):
    """Return traversal cost: hazardous (5) → 5, clear (0) → 1."""
    row, col = position
    cell_value = MAZE[row][col]
    return cell_value if cell_value > 0 else 1


def reconstruct_path(came_from, start, goal):
    """Trace back from goal to start using came_from dict."""
    path = []
    current_position = goal
    while current_position != start:
        path.append(current_position)
        current_position = came_from[current_position]
    path.append(start)
    path.reverse()
    return path
