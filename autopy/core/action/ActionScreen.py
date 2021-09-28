import win32api
import pyautogui as autogui

from autopy.core.action.ActionImage import ActionImage


class ActionScreen:
    @staticmethod
    def change_resolution(params: tuple):
        (width, height) = params
        dm = win32api.EnumDisplaySettings(None, 0)
        dm.PelsWidth = width
        dm.PelsHeight = height
        dm.BitsPerPel = 32
        dm.DisplayFixedOutput = 1  # 0:缺省; 1:居中; 2:拉伸
        win32api.ChangeDisplaySettings(dm, 0)

    @classmethod
    def snapshot(cls, rect):
        """
        根据跟定的ScreenRect区域截图
        :param rect: 遵从一般系统坐标系的矩形区域(左上角为0,0点), autogui和Pillow都适用
        :return:
        """
        screen_shot = autogui.screenshot()
        # rect = rect.swap_top_bottom()
        crop_img = screen_shot.crop(
            (int(float(rect.left)), int(float(rect.top)), int(float(rect.right)), int(float(rect.bottom))))
        return crop_img

    @classmethod
    def snapshot_cv(cls, rect):
        pil_image = cls.snapshot(rect)
        return ActionImage.pil_to_cv(pil_image)

    @staticmethod
    def pick_color(x, y):
        return autogui.pixel(x, y)

    @staticmethod
    def pixel_matches_color(x, y, color_tuple, tolerance=0):
        return autogui.pixelMatchesColor(x, y, color_tuple, tolerance)
