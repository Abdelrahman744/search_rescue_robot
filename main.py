# main.py
# Entry point — runs BFS, DFS, Dijkstra, prints analysis, and shows the maze.

import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from maze import MAZE, ROWS, COLS, START, GOAL, get_cost
from bfs import bfs
from dfs import dfs
from dijkstra import dijkstra


# ── Helpers ──────────────────────────────────────────────────────

def path_cost(path):
    """Total traversal cost of a path (skip the start cell)."""
    return sum(get_cost(cell) for cell in path[1:])


def run_algorithm(name, func, start, goal):
    """Run an algorithm, measure time, return results dict."""
    t0 = time.perf_counter()
    result = func(start, goal)
    elapsed = time.perf_counter() - t0

    # Dijkstra returns 3 values, BFS/DFS return 2
    if len(result) == 3:
        path, explored, cost = result
    else:
        path, explored = result
        cost = path_cost(path) if path else None

    return {
        'name': name,
        'path': path,
        'explored': explored,
        'steps': len(path) if path else 0,
        'cost': cost,
        'time_ms': elapsed * 1000,
    }


# ── Analysis ─────────────────────────────────────────────────────

def print_analysis(results):
    """Print a performance comparison table and summary."""
    line = "=" * 62
    print(f"\n{line}")
    print(f"  {'PERFORMANCE ANALYSIS':^58}")
    print(line)
    print(f"  {'Metric':<25} {'BFS':>10} {'DFS':>10} {'Dijkstra':>10}")
    print(line)

    for label, key, fmt in [
        ("Path length (steps)",  'steps',    'd'),
        ("Total traversal cost", 'cost',     'd'),
        ("Nodes explored",       'explored', 'd'),
        ("Time (ms)",            'time_ms',  '.4f'),
    ]:
        vals = []
        for r in results:
            v = len(r[key]) if key == 'explored' else r[key]
            vals.append(f"{v:>10{fmt}}")
        print(f"  {label:<25} {''.join(vals)}")

    print(line)
    print("""
  SUMMARY
  ---------------------------------------------------------
  Optimality:
    BFS      - Optimal in steps (fewest hops), but ignores cell costs.
    DFS      - Not optimal. Finds a path, not necessarily the shortest.
    Dijkstra - Always optimal. Minimizes total traversal cost.

  Efficiency:
    BFS      - Explores uniformly outward; moderate node count.
    DFS      - May explore fewer nodes if lucky, but wastes effort on wrong branches.
    Dijkstra - Slightly more overhead, but guarantees minimum-cost path.

  Conclusion:
    Dijkstra is the best choice for the rescue robot — it finds the
    safest, lowest-cost route while correctly avoiding hazardous zones.
  ---------------------------------------------------------
""")


# ── Visualization ────────────────────────────────────────────────

COLORS = {
    'wall':   '#2b2b2b',
    'clear':  '#ffffff',
    'hazard': '#f0a500',
    'path':   '#27ae60',
    'start':  '#2980b9',
    'goal':   '#e74c3c',
}


def draw_maze(ax, path, title):
    """Draw one maze with its solution path on the given axes."""
    # Draw cells
    for r in range(ROWS):
        for c in range(COLS):
            v = MAZE[r][c]
            color = COLORS['wall'] if v == 1 else COLORS['hazard'] if v == 5 else COLORS['clear']
            ax.add_patch(plt.Rectangle((c, ROWS - 1 - r), 1, 1, color=color))

    # Draw path
    if path:
        for (r, c) in path:
            if (r, c) not in (START, GOAL):
                ax.add_patch(plt.Rectangle((c, ROWS - 1 - r), 1, 1, color=COLORS['path']))

    # Start and Goal markers
    ax.add_patch(plt.Rectangle((START[1], ROWS - 1 - START[0]), 1, 1, color=COLORS['start']))
    ax.add_patch(plt.Rectangle((GOAL[1],  ROWS - 1 - GOAL[0]),  1, 1, color=COLORS['goal']))
    ax.text(START[1] + 0.5, ROWS - 1 - START[0] + 0.5, 'S',
            ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    ax.text(GOAL[1] + 0.5,  ROWS - 1 - GOAL[0] + 0.5,  'G',
            ha='center', va='center', fontsize=10, fontweight='bold', color='white')

    # Grid lines
    for x in range(COLS + 1):
        ax.axvline(x, color='#cccccc', linewidth=0.5)
    for y in range(ROWS + 1):
        ax.axhline(y, color='#cccccc', linewidth=0.5)

    ax.set_xlim(0, COLS)
    ax.set_ylim(0, ROWS)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=11, fontweight='bold')


def show_results(results):
    """Show all three mazes side by side in one figure."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for ax, r in zip(axes, results):
        draw_maze(ax, r['path'], f"{r['name']}  -  {r['steps']} steps, cost {r['cost']}")

    # Shared legend
    legend = [
        mpatches.Patch(color=COLORS['start'],  label='Start'),
        mpatches.Patch(color=COLORS['goal'],   label='Goal'),
        mpatches.Patch(color=COLORS['path'],   label='Path'),
        mpatches.Patch(color=COLORS['hazard'], label='Hazard (cost 5)'),
        mpatches.Patch(color=COLORS['wall'],   label='Wall'),
    ]
    fig.legend(handles=legend, loc='lower center', ncol=5, fontsize=9)

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.show()


# -- Main ---------------------------------------------------------

def main():
    print("=" * 62)
    print("   Search & Rescue Robot - AI Search Algorithms")
    print("=" * 62)
    print(f"   Start: {START}  ->  Goal: {GOAL}\n")

    results = [
        run_algorithm("BFS",      bfs,      START, GOAL),
        run_algorithm("DFS",      dfs,      START, GOAL),
        run_algorithm("Dijkstra", dijkstra, START, GOAL),
    ]

    print_analysis(results)
    show_results(results)


if __name__ == '__main__':
    main()
