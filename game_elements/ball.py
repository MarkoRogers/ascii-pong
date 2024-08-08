class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 1

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def bounce(self):
        self.dx = -self.dx
        self.dy = -self.dy

    def draw(self, canvas):
        canvas.draw_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, 0xFFFFFF)
