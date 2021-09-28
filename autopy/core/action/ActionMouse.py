import pyautogui


class MousePosition(object):
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y


def click(x, y):
    pyautogui.click(int(x), int(y))


def dbclick(x, y):
    pyautogui.doubleClick(int(x), int(y))


def move(x, y):
    pyautogui.moveTo(int(x), int(y), duration=0.25)


def rightclick(x, y):
    pyautogui.rightClick(int(x), int(y))


def drag(x, y):
    pyautogui.dragTo(int(x), int(y), 0.5)


def scroll(clicks):
    pyautogui.scroll(clicks)


def position():
    pos = pyautogui.position()
    return MousePosition(pos[0], pos[1])
