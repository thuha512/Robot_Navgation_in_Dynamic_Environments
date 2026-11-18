class DynamicObstacle:
    """Moves back and forth along a predefined list of cells."""
    def __init__(self, name, positions, color=None):
        if len(positions) < 2:
            raise ValueError("An obstacle patrol needs at least two positions.")
        self.name = name
        self.positions = [tuple(p) for p in positions]
        self.index = 0
        self.direction = 1
        self.color = color or "#ef5350"

    @property
    def position(self):
        return self.positions[self.index]

    def next_position(self):
        nxt = self.index + self.direction
        if nxt >= len(self.positions):
            return self.positions[self.index - 1]
        if nxt < 0:
            return self.positions[self.index + 1]
        return self.positions[nxt]

    def update(self):
        nxt = self.index + self.direction
        if nxt >= len(self.positions):
            self.direction = -1
            nxt = self.index + self.direction
        elif nxt < 0:
            self.direction = 1
            nxt = self.index + self.direction
        self.index = nxt

    def serialize(self):
        return {"name": self.name, "position": list(self.position),
                "next_position": list(self.next_position()), "color": self.color}

def create_default_obstacles():
    return [
        DynamicObstacle("Horizontal", [(6, c) for c in range(2, 8)], "#ef5350"),
        DynamicObstacle("Vertical", [(r, 10) for r in range(2, 8)], "#ab47bc"),
        DynamicObstacle("Patrol", [(15, 3), (15, 4), (15, 5), (16, 5), (17, 5), (17, 4), (17, 3), (16, 3)], "#ff9800")
    ]
