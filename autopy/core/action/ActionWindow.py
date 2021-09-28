import win32con
import win32gui

from autopy.core.data.ScreenRect import ScreenRect


class ActionWindow:
    @classmethod
    def get_current_window(cls):
        return win32gui.GetForegroundWindow()

    @classmethod
    def set_current_window(cls, hwnd):
        if win32gui.IsIconic(hwnd):
            # 如果窗口被最小化了，先恢复
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)

    @classmethod
    def get_window_title(cls, hwnd):
        return win32gui.GetWindowText(hwnd)

    @classmethod
    def get_window_class(cls, hwnd):
        return win32gui.GetClassName(hwnd)

    @classmethod
    def get_current_window_title(cls):
        return cls.get_window_title(cls.get_current_window())

    @classmethod
    def find_window(cls, title=None, win_class=None):
        try:
            return win32gui.FindWindow(win_class, title)
        except Exception as ex:
            print('error calling win32gui.FindWindow ' + str(ex))
            return None

    @classmethod
    def get_window_rect(cls, hwnd):
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        return ScreenRect(left, right, top, bottom)

    @classmethod
    def set_window_pos(cls, hwnd, x, y, width, height):
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, width, height, win32con.SWP_SHOWWINDOW)
