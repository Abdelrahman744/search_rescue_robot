# Problem Formulation — Search & Rescue Robot (Maze Navigator)

## 1. Problem Description

An autonomous rescue robot is deployed into a disaster zone modeled as a 2D grid
maze. The robot's mission is to navigate from its deployment point to the location
of a trapped survivor. The environment contains clear paths, impassable walls and
debris, and hazardous areas (e.g., muddy or chemically contaminated zones) that
are traversable but carry a higher movement cost.

Three uninformed/informed search algorithms — **BFS**, **DFS**, and **Dijkstra** —
are used to find a path from the robot's starting position to the survivor's
location, and their performance is compared.

---

## 2. PEAS Description

| Component             | Definition                                                                                                                                                   |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Performance Measure** | 1. **Path cost minimization** — reach the survivor with the lowest total traversal cost (clear cells cost 1, hazardous cells cost 5). 2. **Path length** — minimize the number of steps taken. 3. **Efficiency** — minimize the number of cells explored before reaching the goal. |
| **Environment**        | A **10 × 10 two-dimensional grid**. Each cell is one of three types: **Clear path** (value `0`, cost 1) — safe to traverse. **Wall / debris** (value `1`) — completely impassable. **Hazardous zone** (value `5`, cost 5) — traversable but dangerous (higher cost). The environment is **fully observable**, **static**, **discrete**, **deterministic**, and **single-agent**. |
| **Actuators**          | The robot can move in **four cardinal directions**: **Up** (row − 1), **Down** (row + 1), **Left** (col − 1), **Right** (col + 1). Each move transitions the robot from its current cell to an adjacent cell (if that cell is within bounds and is not a wall). |
| **Sensors**            | The robot can sense: 1. Its **current position** (row, col) on the grid. 2. The **type of each neighboring cell** (clear, wall, or hazardous). 3. Whether it has **reached the goal** cell (survivor location). |

---

## 3. State Space

### Representation

The environment is represented as a **2D array (list of lists)** of integers:

```
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
```

- **Cell values:** `0` = clear path (cost 1), `1` = wall (impassable), `5` = hazardous zone (cost 5).
- **Grid dimensions:** 10 rows × 10 columns = **100 total cells**.
- **Reachable states:** Every non-wall cell is a valid state the robot can occupy.

### State Definition

Each **state** is a tuple `(row, col)` representing the robot's current position
on the grid, where `0 ≤ row < 10` and `0 ≤ col < 10`.

---

## 4. States & Actions

### Initial State

```
START = (0, 0)   — Top-left corner (robot deployment point)
```

### Goal State

```
GOAL = (9, 9)    — Bottom-right corner (trapped survivor location)
```

The goal test checks whether the robot's current position equals `(9, 9)`.

### Valid Actions

The robot can perform **four actions** at any state `(r, c)`:

| Action     | Direction Vector | Resulting State  | Condition                                      |
|------------|-----------------|------------------|-------------------------------------------------|
| Move Up    | `(-1,  0)`      | `(r − 1, c)`    | `r − 1 ≥ 0` and target cell is not a wall (`≠ 1`) |
| Move Down  | `(+1,  0)`      | `(r + 1, c)`    | `r + 1 < 10` and target cell is not a wall (`≠ 1`) |
| Move Left  | `( 0, -1)`      | `(r, c − 1)`    | `c − 1 ≥ 0` and target cell is not a wall (`≠ 1`) |
| Move Right | `( 0, +1)`      | `(r, c + 1)`    | `c + 1 < 10` and target cell is not a wall (`≠ 1`) |

An action is **valid** only if:
1. The resulting cell is **within the grid boundaries**.
2. The resulting cell is **not a wall** (cell value ≠ 1).

### Transition Model

Applying a valid action to state `(r, c)` deterministically moves the robot to the
new state `(r + dr, c + dc)` with a **transition cost** equal to the destination
cell's value:
- Moving into a **clear cell** (value `0`) costs **1**.
- Moving into a **hazardous cell** (value `5`) costs **5**.

---

## 5. Environment Properties Summary

| Property          | Value            | Explanation                                              |
|-------------------|------------------|----------------------------------------------------------|
| Observable        | Fully observable | The robot has complete knowledge of the entire grid      |
| Deterministic     | Yes              | Each action has a single guaranteed outcome              |
| Episodic          | Yes              | The task ends when the goal is reached                   |
| Static            | Yes              | The maze does not change while the robot is navigating   |
| Discrete          | Yes              | Finite number of states and actions                      |
| Single-agent      | Yes              | Only one robot is navigating the maze                    |

---

## 6. Performance Analysis

### Results

| Metric              | BFS   | DFS   | Dijkstra |
|---------------------|-------|-------|----------|
| Path length (steps) | 19    | 37    | 19       |
| Total traversal cost| 18    | 44    | 18       |
| Nodes explored      | 58    | 37    | 57       |

### Optimality

- **BFS** found the shortest path in terms of number of steps (19 steps), because it explores the maze level by level and always finds the path with the fewest hops. However, BFS treats all edges as equal and does not account for cell costs.
- **DFS** found a valid path but not the shortest one (37 steps, cost 44). DFS goes as deep as possible before backtracking, so it often takes a longer, suboptimal route. It is **not optimal** by design.
- **Dijkstra** also found a 19-step path with cost 18 — the same as BFS in this maze. Dijkstra is **always optimal** for weighted graphs because it expands nodes by lowest cumulative cost, guaranteeing the minimum-cost path.

### Efficiency

- **BFS** explored 58 nodes. It expands uniformly in all directions, which leads to a moderate number of explored nodes.
- **DFS** explored only 37 nodes — the fewest — because it commits to a single deep path before trying alternatives. However, this efficiency comes at the expense of optimality.
- **Dijkstra** explored 57 nodes, similar to BFS, since both systematically cover the search space. Dijkstra has slightly more overhead per node due to the priority queue, but the difference is negligible on a small grid.

### Conclusion

Dijkstra is the best choice for the rescue robot. It guarantees the lowest-cost path while correctly handling hazardous zones with higher traversal costs. BFS is a good alternative when all cells have equal cost, and DFS is the least suitable since it does not guarantee an optimal path.
