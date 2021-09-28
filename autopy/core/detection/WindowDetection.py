from autopy.core.action.ActionWindow import ActionWindow
from autopy.core.data.ScreenRect import ScreenRect
from autopy.core.detection.Detection import Detection


class WindowResult:
    hwnd: int

    def __init__(self, hwnd):
        self.hwnd = hwnd


class WindowDetection(Detection):
    current_only: True
    win_class: ScreenRect
    title: str

    def do(self, find_all=False):
        if self.current_only:
            check_pass = True
            hwnd = ActionWindow.get_current_window()
            msg = ''
            if self.title:
                title = ActionWindow.get_window_title(hwnd)
                if title != self.title:
                    check_pass = check_pass or False
                else:
                    check_pass = check_pass or True
                if self.debug:
                    msg += '实际title:"{}", 预期title:"{}"'.format(title, self.title)

            if self.win_class:
                win_class = ActionWindow.get_window_class(hwnd)
                if win_class != self.win_class:
                    check_pass = check_pass or False
                else:
                    check_pass = check_pass or True
                if self.debug:
                    msg += '' if msg=='' else ', '
                    msg += '实际class:"{}", 预期class:"{}"'.format(win_class, self.win_class)

            if check_pass:
                if self.debug:
                    print('检查当前窗口成功，{}'.format(msg))
                return WindowResult(hwnd)
            else:
                if self.debug:
                    print('检查当前窗口失败，{}'.format(msg))
                return None
        else:
            hwnd = ActionWindow.find_window(self.title, self.win_class)
            if hwnd is None:
                if self.debug:
                    print('检测窗口失败，预期title:"{}", 预期class:"{}'.format(self.title, self.win_class))
                return None
            else:
                if self.debug:
                    print('检测窗口成功，预期title:"{}", 预期class:"{}'.format(self.title, self.win_class))
                ActionWindow.set_current_window(hwnd)
                return WindowResult(hwnd)

