from .ScreenRect import ScreenRect


class ImageDetection:
    snapshot: ScreenRect
    template: str


class OcrDetection:
    snapshot: ScreenRect
    text: str


class Action:
    def __init__(self, action_str):
        self._action_str = action_str


class Check:
    image: ImageDetection
    ocr: OcrDetection
    fail_action: Action


class For:
    def __init__(self, _for_str):
        self._for_str = _for_str


class To:
    def __init__(self, _to_str):
        self._to_str = _to_str
        self.state = None

    def parse(self):
        self.state = State()


class Transition:
    foreach: For
    action: Action
    wait: int
    to: To


class Scroll:
    one_page: int  # 每页滚动的距离，单位是虚拟像素（根据屏幕分辨率可能有缩放）
    page_count: int  # 滚动页数


class Find:
    image: ImageDetection
    ocr: OcrDetection
    scroll: Scroll
    fail_action: Action
    transition: Transition
    find_all: bool


class State:
    name: str = None
    id: int = -1
    check: Check
    find: Find
    transition: Transition


Transition.to = State()
