import ctypes
import ctypes.wintypes
import time

# Constants
WM_DESTROY = 0x0002
WM_CLOSE = 0x0010
WM_QUIT = 0x0012
WM_PAINT = 0x000F
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
VK_UP = 0x26
VK_DOWN = 0x28

# Define Windows API functions
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32

GetModuleHandleW = kernel32.GetModuleHandleW
GetModuleHandleW.restype = ctypes.wintypes.HMODULE
GetModuleHandleW.argtypes = [ctypes.wintypes.LPCWSTR]

# Manually define missing wintypes
HCURSOR = ctypes.wintypes.HANDLE
HICON = ctypes.wintypes.HANDLE
HBRUSH = ctypes.wintypes.HANDLE


# Define the WNDCLASS structure
class WNDCLASS(ctypes.Structure):
    _fields_ = [("style", ctypes.c_uint),
                ("lpfnWndProc",
                 ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM,
                                    ctypes.wintypes.LPARAM)),
                ("cbClsExtra", ctypes.c_int),
                ("cbWndExtra", ctypes.c_int),
                ("hInstance", ctypes.wintypes.HINSTANCE),
                ("hIcon", HICON),
                ("hCursor", HCURSOR),
                ("hbrBackground", HBRUSH),
                ("lpszMenuName", ctypes.wintypes.LPCWSTR),
                ("lpszClassName", ctypes.wintypes.LPCWSTR)]


RegisterClassW = user32.RegisterClassW
RegisterClassW.restype = ctypes.wintypes.ATOM
RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASS)]

CreateWindowExW = user32.CreateWindowExW
CreateWindowExW.restype = ctypes.wintypes.HWND
CreateWindowExW.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.LPCWSTR, ctypes.wintypes.LPCWSTR,
                            ctypes.wintypes.DWORD, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                            ctypes.wintypes.HWND, ctypes.wintypes.HMENU, ctypes.wintypes.HINSTANCE, ctypes.c_void_p]

ShowWindow = user32.ShowWindow
ShowWindow.restype = ctypes.wintypes.BOOL
ShowWindow.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]

UpdateWindow = user32.UpdateWindow
UpdateWindow.restype = ctypes.wintypes.BOOL
UpdateWindow.argtypes = [ctypes.wintypes.HWND]

DefWindowProcW = user32.DefWindowProcW
DefWindowProcW.restype = ctypes.c_long
DefWindowProcW.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM]

PeekMessageW = user32.PeekMessageW
PeekMessageW.restype = ctypes.wintypes.BOOL
PeekMessageW.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG), ctypes.wintypes.HWND, ctypes.wintypes.UINT,
                         ctypes.wintypes.UINT, ctypes.wintypes.UINT]

TranslateMessage = user32.TranslateMessage
TranslateMessage.restype = ctypes.wintypes.BOOL
TranslateMessage.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]

DispatchMessageW = user32.DispatchMessageW
DispatchMessageW.restype = ctypes.c_long
DispatchMessageW.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]


# Define the SimpleWindow class
class SimpleWindow:
    def __init__(self, width, height, title="SimpleWindow"):
        print("Initializing SimpleWindow")
        self.width = width
        self.height = height
        self.title = title
        self.hwnd = self.create_window()
        self.is_running = True
        self.keys = set()

    def create_window(self):
        wc_name = "SimpleWindowClass"

        WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM,
                                     ctypes.wintypes.LPARAM)

        wc = WNDCLASS()
        wc.lpszClassName = wc_name
        wc.lpfnWndProc = WNDPROC(self.wnd_proc)
        wc.hInstance = GetModuleHandleW(None)
        wc.hbrBackground = gdi32.GetStockObject(1)
        wc.hCursor = user32.LoadCursorW(None, 32512)
        wc.hIcon = user32.LoadIconW(None, 32512)
        wc.style = 3

        print("Registering window class")
        if not RegisterClassW(ctypes.byref(wc)):
            raise Exception("Window Registration Failed")

        hwnd = CreateWindowExW(
            0,
            wc_name,
            self.title,
            13565952,
            100, 100,
            self.width, self.height,
            0, 0, wc.hInstance, 0
        )

        if not hwnd:
            raise Exception("Window Creation Failed")

        ShowWindow(hwnd, 5)
        UpdateWindow(hwnd)
        print("Window created successfully")
        return hwnd

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        print(f"wnd_proc called: msg={msg}")
        if msg == WM_DESTROY:
            print("WM_DESTROY received")
            user32.PostQuitMessage(0)
            self.is_running = False
        elif msg == WM_KEYDOWN:
            print(f"Key down: {wparam}")
            self.keys.add(wparam)
        elif msg == WM_KEYUP:
            print(f"Key up: {wparam}")
            self.keys.discard(wparam)
        elif msg == WM_CLOSE:
            print("WM_CLOSE received")
            user32.DestroyWindow(hwnd)
        return DefWindowProcW(hwnd, msg, wparam, lparam)

    def handle_events(self):
        msg = ctypes.wintypes.MSG()
        while PeekMessageW(ctypes.byref(msg), 0, 0, 0, 1):
            if msg.message == WM_QUIT:
                print("WM_QUIT received")
                self.is_running = False
            TranslateMessage(ctypes.byref(msg))
            DispatchMessageW(ctypes.byref(msg))

    def mainloop(self, update_func):
        print("Entering main loop")
        while self.is_running:
            self.handle_events()
            update_func()
            time.sleep(0.016)  # ~60 FPS
        print("Exiting main loop")


# Example update function
def update():
    print("Updating...")


if __name__ == "__main__":
    window = SimpleWindow(800, 600, "Test Window")
    window.mainloop(update)
