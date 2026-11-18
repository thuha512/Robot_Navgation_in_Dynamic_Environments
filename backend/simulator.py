from environment import Environment
from robot import Robot
from obstacles import create_default_obstacles
from replanning import Replanner

class Simulator:
    def __init__(self):
        self.reset()

    def reset(self, config=None):
        config = config or {}
        self.environment = Environment()
        if config.get("start") is not None and config.get("goal") is not None:
            self.environment.set_start_goal(tuple(config["start"]), tuple(config["goal"]))
        if "static_obstacles" in config:
            self.environment.static_obstacles = {
                tuple(p) for p in config["static_obstacles"]
                if tuple(p) not in (self.environment.start, self.environment.goal)
                and self.environment.grid.in_bounds(tuple(p))
            }
        self.robot = Robot(self.environment.start)
        self.obstacles = create_default_obstacles()
        self.replanner = Replanner()
        self.time_step = 0
        self.running = False
        self.paused = False
        self.last_event = "Simulation reset"
        self.last_nodes_explored = 0
        self.initial_plan()

    def dynamic_positions(self):
        return {o.position for o in self.obstacles}

    def initial_plan(self):
        path, explored = self.replanner.plan(self.environment, self.robot, self.obstacles)
        self.last_nodes_explored = explored
        self.last_event = "Initial path found" if path is not None else "No path available"

    def start(self):
        if self.robot.reached_goal:
            self.last_event = "Robot has already reached the goal"
            return
        self.running = True
        self.paused = False
        self.last_event = "Simulation started"

    def pause(self):
        self.paused = True
        self.last_event = "Simulation paused"

    def step(self):
        if self.robot.reached_goal:
            self.running = False
            self.last_event = "Goal reached"
            return self.snapshot()

        # Predict obstacle positions before committing their movement.
        old_positions = self.dynamic_positions()
        next_positions = {o.next_position() for o in self.obstacles}
        next_robot_cell = self.robot.next_position()

        # Move obstacles, then validate the remaining robot path against their new positions.
        for obstacle in self.obstacles:
            obstacle.update()
        new_positions = self.dynamic_positions()

        if self.replanner.path_is_blocked(self.robot, self.obstacles):
            path, explored = self.replanner.plan(self.environment, self.robot, self.obstacles)
            self.last_nodes_explored = explored
            self.last_event = "Replanning: a moving obstacle blocked the current path"
            if path is None:
                self.last_event = "No safe path currently available"
                self.running = False
                self.time_step += 1
                return self.snapshot()

        # Prevent stepping into a currently occupied cell or swapping positions with an obstacle.
        next_robot_cell = self.robot.next_position()
        swap_collision = any(
            next_robot_cell == old and self.robot.position == new
            for old, new in zip(old_positions, [o.position for o in self.obstacles])
        ) if next_robot_cell is not None else False

        if next_robot_cell is not None and (next_robot_cell in new_positions or swap_collision):
            path, explored = self.replanner.plan(self.environment, self.robot, self.obstacles)
            self.last_nodes_explored = explored
            self.last_event = "Replanning: predicted collision"
        else:
            moved = self.robot.move_one_step(new_positions)
            if moved:
                self.last_event = "Robot moved one cell"
            elif self.robot.path:
                path, explored = self.replanner.plan(self.environment, self.robot, self.obstacles)
                self.last_nodes_explored = explored
                self.last_event = "Replanning: next cell became blocked"

        self.time_step += 1
        if self.robot.reached_goal:
            self.running = False
            self.last_event = "Goal reached successfully"
        return self.snapshot()

    def snapshot(self):
        return {
            "environment": self.environment.serialize(),
            "robot": self.robot.serialize(),
            "dynamic_obstacles": [o.serialize() for o in self.obstacles],
            "path": [list(p) for p in self.robot.path],
            "time_step": self.time_step,
            "running": self.running,
            "paused": self.paused,
            "replanning_count": self.replanner.replanning_count,
            "total_nodes_explored": self.replanner.total_nodes_explored,
            "last_nodes_explored": self.last_nodes_explored,
            "path_length": self.robot.steps_taken + len(self.robot.path),
            "steps_taken": self.robot.steps_taken,
            "status": self.robot.status,
            "event": self.last_event
        }
