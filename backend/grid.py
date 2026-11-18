class Grid:
    """20x20 grid. Coordinates use (row, col)."""
    def __init__(self, rows=20, cols=20):
        self.rows = rows
        self.cols = cols

    def in_bounds(self, position):
        r, c = position
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, position):
        r, c = position
        candidates = [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]
        return [p for p in candidates if self.in_bounds(p)]
