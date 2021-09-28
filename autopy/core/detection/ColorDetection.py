from typing import Tuple

from autopy.core.action.ActionScreen import ActionScreen
from autopy.core.detection.Detection import Detection


class ColorDetection(Detection):
    pos: Tuple[int, int]
    color: Tuple[int, int, int]
    tolerance: int = 0

    def do(self, find_all=False):
        x, y = self.pos
        pix = ActionScreen.pick_color(x, y)
        tolerance = self.tolerance
        r, g, b = pix[:3]
        exR, exG, exB = self.color
        diff = abs(r - exR) + abs(g - exG) + abs(b - exB)

        if self.debug:
            print("检测颜色{}，坐标点({},{}) 颜色{}，与预期颜色({},{},{})差异值‘{}’".format(
                '成功' if diff <= tolerance else '失败',
                x, y,
                pix,
                r, g, b,
                diff
            ))
        if diff <= tolerance:
            return diff
        else:
            return None
