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


class Transition:
    pass


class Scroll:
    pass


class Find:
    image: ImageDetection
    ocr: OcrDetection
    scroll: Scroll
    fail_action: Action
    transition: Transition


class State:
    name: str = None
    id: int = -1
    check: Check
    find: Find
    transition: Transition
