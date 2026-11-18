import heapq

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_search(environment, start, goal, dynamic_obstacles=None):
    """Return (path, nodes_explored). Path excludes start and includes goal."""
    start, goal = tuple(start), tuple(goal)
    blocked = set(environment.static_obstacles)
    blocked.update(tuple(p) for p in (dynamic_obstacles or []))
    blocked.discard(start)

    if start == goal:
        return [], 0
    if not environment.grid.in_bounds(start) or not environment.grid.in_bounds(goal):
        return None, 0
    if goal in blocked:
        return None, 0

    frontier = [(manhattan(start, goal), 0, start)]
    came_from = {start: None}
    g_score = {start: 0}
    explored = 0
    counter = 0

    while frontier:
        _, _, current = heapq.heappop(frontier)
        explored += 1
        if current == goal:
            path = []
            node = goal
            while node != start:
                path.append(node)
                node = came_from[node]
            path.reverse()
            return path, explored

        for neighbor in environment.grid.neighbors(current):
            if neighbor in blocked:
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                counter += 1
                f = tentative_g + manhattan(neighbor, goal)
                heapq.heappush(frontier, (f, counter, neighbor))

    return None, explored
