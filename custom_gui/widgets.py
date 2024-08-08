import ctypes


class Canvas:
    def __init__(self, window):
        self.hwnd = window.hwnd
        self.hdc = ctypes.windll.user32.GetDC(self.hwnd)

    def draw_rectangle(self, x1, y1, x2, y2, color):
        brush = ctypes.windll.gdi32.CreateSolidBrush(color)
        rect = ctypes.wintypes.RECT(x1, y1, x2, y2)
        ctypes.windll.user32.FillRect(self.hdc, ctypes.byref(rect), brush)
        ctypes.windll.gdi32.DeleteObject(brush)

    def draw_oval(self, x1, y1, x2, y2, color):
        brush = ctypes.windll.gdi32.CreateSolidBrush(color)
        pen = ctypes.windll.gdi32.CreatePen(0, 1, color)
        ctypes.windll.gdi32.SelectObject(self.hdc, pen)
        ctypes.windll.gdi32.SelectObject(self.hdc, brush)
        ctypes.windll.gdi32.Ellipse(self.hdc, x1, y1, x2, y2)
        ctypes.windll.gdi32.DeleteObject(brush)
        ctypes.windll.gdi32.DeleteObject(pen)

    def clear(self):
        ctypes.windll.gdi32.Rectangle(self.hdc, 0, 0, 800, 600)
