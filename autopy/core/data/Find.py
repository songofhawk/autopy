from __future__ import annotations

import time

from autopy.core.action import ActionMouse
from autopy.core.data.Action import Execution, Action
from autopy.core.detection.ImageDetection import ImageDetection
from autopy.core.detection.OcrDetection import OcrDetection
from autopy.core.detection.ColorDetection import ColorDetection
from autopy.core.detection.WindowDetection import WindowDetection


class Scroll:
    """
    在查找（Find）过程中的滚动配置
    Attributes:
        one_page (int): 每页滚动的距离，单位是虚拟像素（根据屏幕分辨率可能有缩放）
        page_count (int): 滚动页数
        find_mode (str): 是否要在滚动的过程中，找出所有结果，缺省为"Any"；
        如果为"All"，表示要完成所有滚动，并且在每一页执行detection，保存检测结果；
        如果为"Any"，则只要有一页检测通过，就不再滚动了
    """
    one_page: int  #
    page_count: int  #
    find_mode: str = "Any"


class Find:
    """
    用于查找的基础配置，可以有不同的查找模式，在State节点中，它如果是check属性，则不保存查找结果，如果是find属性，则把查找结果，临时存入find_result

    Attributes:
        image (ImageDetection) : 图像检测，在当前页面中找指定图像片段，不一定要完全一致，可以指定相似度
        ocr (OcrDetection) : 文本检测，在当前页面的指定位置做OCR识别，然后查看是否有指定的文本
        color (ColorDetection) : 颜色检测，在当前页面的指定像素位置，查看是否符合定义的颜色
        window (WindowDetection) : 窗口检测，在当前页面查找指定title或者name的窗口

        scroll (Scroll) : 查找的时候，如果没找到，就滚动当前窗口，继续查找
        fail_action (Execution) : 如果什么没有找到，需要执行的操作
        result_name (str): 给检测结果一个变量名
    """
    image: ImageDetection
    ocr: OcrDetection
    color: ColorDetection
    window: WindowDetection
    scroll: Scroll
    fail_action: Execution
    result_name: None

    def do(self):
        if self.image is not None:
            return self._do_once(self.image)
        elif self.ocr is not None:
            return self._do_once(self.ocr)
        elif self.color is not None:
            return self._do_once(self.color)
        elif self.window is not None:
            return self._do_once(self.window)

    def _do_once(self, detection):
        if detection is None:
            return None
        detect_res = None
        results = []
        page = 0
        if self.scroll is not None:
            # 有滚动的话，就按滚动页数执行循环
            count = self.scroll.page_count
            find_all = (self.scroll.find_mode == "All")
        else:
            # 没有滚动的话，就只执行一次
            count = 1
            find_all = True
        while page < count and (
                (not find_all and detect_res is None)
                or
                find_all
        ):
            # 如果滚动的时候，找到即返回，那么就检查detect_res是否为None
            # 如果滚动到指定页数，返回所有找到的结果，那么就不用检查detect_res了
            detect_res = detection.do()
            if isinstance(detect_res, list):
                results.extend(detect_res)
            else:
                results.append(detect_res)
            page += 1
            if self.scroll:
                time.sleep(1)
                # print('before scroll {}'.format(self.scroll.one_page))
                ActionMouse.scroll(self.scroll.one_page)
                # print('-- after scroll')

        size = len(results)
        if size == 0:
            Action.call(self.fail_action)
            return None
        elif size == 1:
            return results[0]
        else:
            return results
