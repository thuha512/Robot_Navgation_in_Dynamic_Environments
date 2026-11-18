class Robot:
    def __init__(self, start_position):
        self.position = tuple(start_position)
        self.path = []
        self.steps_taken = 0
        self.reached_goal = False
        self.status = "Ready"

    def set_path(self, path):
        self.path = list(path or [])
        self.reached_goal = False
        self.status = "Moving" if self.path else "No path"

    def next_position(self):
        return self.path[0] if self.path else None

    def move_one_step(self, blocked_positions):
        if not self.path:
            return False
        next_pos = tuple(self.path[0])
        if next_pos in set(blocked_positions):
            self.status = "Blocked"
            return False
        self.position = next_pos
        self.path.pop(0)
        self.steps_taken += 1
        self.status = "Moving" if self.path else "Arrived"
        self.reached_goal = not self.path
        return True

    def serialize(self):
        return {
            "position": list(self.position),
            "path": [list(p) for p in self.path],
            "steps_taken": self.steps_taken,
            "reached_goal": self.reached_goal,
            "status": self.status
        }
