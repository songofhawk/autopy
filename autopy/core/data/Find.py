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
    """
    用于查找的基础配置，可以有不同的查找模式，在State节点中，它如果是check属性，则不保存查找结果，如果是find属性，则把查找结果，临时存入find_result

    Attributes:
        image (ImageDetection) : 图像检测，在当前页面中找指定图像片段，不一定要完全一致，可以指定相似度
        ocr (OcrDetection) : 文本检测，在当前页面的指定位置做OCR识别，然后查看是否有指定的文本
        color (ColorDetection) : 颜色检测，在当前页面的指定像素位置，查看是否符合定义的颜色
        window (WindowDetection) : 窗口检测，在当前页面查找指定title或者name的窗口

        scroll (Scroll) : 查找的时候，如果没找到，就滚动当前窗口，继续查找
        fail_action (Execution) : 如果没有找到，需要执行的操作
        find_all (bool) : 是否查找所有符合检测条件的结果，缺省为False，如果设置为True，那么find_result就是一个列表
    """
    image: ImageDetection
    ocr: OcrDetection
    color: ColorDetection
    window: WindowDetection
    scroll: Scroll
    fail_action: Execution
    find_all: bool = False
    result_name: None

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
