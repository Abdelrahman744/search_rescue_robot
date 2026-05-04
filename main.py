

from maze import MAZE, ROWS, COLS, START, GOAL, get_cost
from bfs import bfs
from dfs import dfs
from dijkstra import dijkstra
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def path_cost(path):
    return sum(get_cost(cell) for cell in path[1:])


def draw_maze(ax, path, title):
    for r in range(ROWS):
        for c in range(COLS):
            v = MAZE[r][c]
            if v == 1:
                color = '#2b2b2b'     # wall
            elif v == 5:
                color = '#f0a500'     # hazard
            else:
                color = '#ffffff'     # clear
            ax.add_patch(plt.Rectangle((c, ROWS-1-r), 1, 1, color=color))

    if path:
        for r, c in path:
            if (r, c) not in (START, GOAL):
                ax.add_patch(plt.Rectangle((c, ROWS-1-r), 1, 1, color='#27ae60'))

    # start & goal
    ax.add_patch(plt.Rectangle((START[1], ROWS-1-START[0]), 1, 1, color='#2980b9'))
    ax.add_patch(plt.Rectangle((GOAL[1], ROWS-1-GOAL[0]), 1, 1, color='#e74c3c'))
    ax.text(START[1]+0.5, ROWS-1-START[0]+0.5, 'S', ha='center', va='center', fontweight='bold', color='white')
    ax.text(GOAL[1]+0.5, ROWS-1-GOAL[0]+0.5, 'G', ha='center', va='center', fontweight='bold', color='white')

    ax.set_xlim(0, COLS)
    ax.set_ylim(0, ROWS)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontweight='bold')


def main():
    print("=" * 50)
    print("  Search & Rescue Robot - AI Search Algorithms")
    print("=" * 50)
    print(f"  Start: {START}  ->  Goal: {GOAL}\n")

    # run algorithms
    bfs_path, bfs_explored = bfs(START, GOAL)
    dfs_path, dfs_explored = dfs(START, GOAL)
    dij_path, dij_explored, dij_cost = dijkstra(START, GOAL)

    # print results
    for name, path, explored in [
        ("BFS", bfs_path, bfs_explored),
        ("DFS", dfs_path, dfs_explored),
        ("Dijkstra", dij_path, dij_explored),
    ]:
        cost = dij_cost if name == "Dijkstra" else path_cost(path)
        print(f"  {name}:  {len(path)} steps, cost {cost}, explored {len(explored)} nodes")

    print("=" * 50)

    # visualize
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, (name, path) in zip(axes, [("BFS", bfs_path), ("DFS", dfs_path), ("Dijkstra", dij_path)]):
        cost = dij_cost if name == "Dijkstra" else path_cost(path)
        draw_maze(ax, path, f"{name} — {len(path)} steps, cost {cost}")

    legend = [
        mpatches.Patch(color='#2980b9', label='Start'),
        mpatches.Patch(color='#e74c3c', label='Goal'),
        mpatches.Patch(color='#27ae60', label='Path'),
        mpatches.Patch(color='#f0a500', label='Hazard'),
        mpatches.Patch(color='#2b2b2b', label='Wall'),
    ]
    fig.legend(handles=legend, loc='lower center', ncol=5)
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.show()


if __name__ == '__main__':
    main()
