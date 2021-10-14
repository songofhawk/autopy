from autopy.core.data.AutoBase import AutoBase


class Detection(AutoBase):
    """
    检测基础类，有ColorDetection, ImageDetection, OcrDetection, WindowDetection等子类，用于检测页面上的特定内容。

    """
    template: str

    def __init__(self):
        self.project = None
        self._template_full_path = None

    def _get_template_full_path(self):
        if self._template_full_path is not None:
            pass
        elif self.project.path_root is not None:
            self._template_full_path = self.project.path_root + '/' + self.template
        else:
            self._template_full_path = self.template

        return self._template_full_path
