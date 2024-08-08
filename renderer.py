class GridRenderer:
    def __init__(self, width, height, fill_char=' '):
        self.width = width
        self.height = height
        self.grid = [[fill_char for _ in range(width)] for _ in range(height)]

    def set_cell(self, x, y, char):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = char

    def render(self):
        import os
        import time
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        for row in self.grid:
            print(''.join(row))
        time.sleep(0.05)  # Control the frame rate
