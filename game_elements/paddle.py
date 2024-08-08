class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, canvas):
        canvas.draw_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, 0xFFFFFF)

    def move(self, dy, max_height):
        self.y += dy
        # Ensure the paddle stays within bounds
        if self.y < 0:
            self.y = 0
        elif self.y > max_height - self.height:
            self.y = max_height - self.height
