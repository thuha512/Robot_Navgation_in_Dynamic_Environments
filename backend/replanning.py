from astar import astar_search

class Replanner:
    def __init__(self):
        self.replanning_count = 0
        self.total_nodes_explored = 0

    def plan(self, environment, robot, obstacles):
        blocked = {o.position for o in obstacles}
        path, explored = astar_search(environment, robot.position, environment.goal, blocked)
        self.total_nodes_explored += explored
        self.replanning_count += 1
        robot.set_path(path)
        return path, explored

    def path_is_blocked(self, robot, obstacles):
        blocked = {o.position for o in obstacles}
        return any(tuple(p) in blocked for p in robot.path)

    def reset(self):
        self.replanning_count = 0
        self.total_nodes_explored = 0
