from grid import Grid

class Environment:
    def __init__(self, rows=20, cols=20, start=(0, 0), goal=(19, 19)):
        self.grid = Grid(rows, cols)
        self.start = tuple(start)
        self.goal = tuple(goal)
        self.static_obstacles = set()
        self.reset_default_obstacles()

    def reset_default_obstacles(self):
        # Two short walls; they leave multiple routes to the goal.
        self.static_obstacles = {
            (4, c) for c in range(3, 10)
        } | {
            (r, 12) for r in range(8, 15)
        }
        self.static_obstacles.discard(self.start)
        self.static_obstacles.discard(self.goal)

    def is_valid(self, position, dynamic_obstacles=None):
        if not self.grid.in_bounds(position):
            return False
        if position in self.static_obstacles:
            return False
        if dynamic_obstacles and position in dynamic_obstacles:
            return False
        return True

    def add_obstacle(self, position):
        position = tuple(position)
        if self.grid.in_bounds(position) and position not in (self.start, self.goal):
            self.static_obstacles.add(position)
            return True
        return False

    def remove_obstacle(self, position):
        self.static_obstacles.discard(tuple(position))

    def set_start_goal(self, start, goal):
        start, goal = tuple(start), tuple(goal)
        if not self.grid.in_bounds(start) or not self.grid.in_bounds(goal):
            raise ValueError("Start/Goal must be inside the grid.")
        if start in self.static_obstacles or goal in self.static_obstacles:
            raise ValueError("Start/Goal cannot be placed on a static obstacle.")
        if start == goal:
            raise ValueError("Start and Goal must be different.")
        self.start, self.goal = start, goal

    def serialize(self):
        return {
            "rows": self.grid.rows,
            "cols": self.grid.cols,
            "start": list(self.start),
            "goal": list(self.goal),
            "static_obstacles": [list(p) for p in sorted(self.static_obstacles)]
        }
