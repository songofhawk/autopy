from __future__ import annotations

import time

from autopy.core.action import ActionMouse
from autopy.core.data.Action import Execution
from autopy.core.detection.ImageDetection import ImageDetection
from autopy.core.detection.OcrDetection import OcrDetection
from autopy.core.detection.ColorDetection import ColorDetection
from autopy.core.detection.WindowDetection import WindowDetection


class Scroll:
    one_page: int  # 每页滚动的距离，单位是虚拟像素（根据屏幕分辨率可能有缩放）
    page_count: int  # 滚动页数


class Find:
    image: ImageDetection
    ocr: OcrDetection
    color: ColorDetection
    window: WindowDetection
    scroll: Scroll
    fail_action: Execution
    find_all: bool = False

    def do(self, exe_fail_action=True):
        if self.image is not None:
            return self._one_detection(self.image, exe_fail_action)
        elif self.ocr is not None:
            return self._one_detection(self.ocr, exe_fail_action)
        elif self.color is not None:
            return self._one_detection(self.color, exe_fail_action)
        elif self.window is not None:
            return self._one_detection(self.window, exe_fail_action)

    def _one_detection(self, detection, exe_fail_action):
        if detection is None:
            return None
        found = detection.do(self.find_all)
        if self.scroll is not None:
            page = 0
            count = self.scroll.page_count
            while not found and page < count:
                # print('before scroll {}'.format(self.scroll.one_page))
                ActionMouse.scroll(self.scroll.one_page)
                # print('-- after scroll')
                time.sleep(1)
                found = detection.do(self.find_all)
                page += 1

        if found is None and self.fail_action is not None and exe_fail_action:
            self.fail_action.call()
            return None
        return found
