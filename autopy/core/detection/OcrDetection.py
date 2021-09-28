from autopy.core.action.ActionScreen import ActionScreen
from autopy.core.action.ActionImage import ActionImage
from autopy.core.data.ScreenRect import ScreenRect
from autopy.core.detection.Detection import Detection


class OcrDetection(Detection):
    snapshot: ScreenRect
    text: str
    confidence: float = 0.8

    def do(self, find_all=False):
        image_current = ActionScreen.snapshot(self.snapshot.evaluate())
        confidence, text = self.text_similar(self.text, image_current)
        if confidence >= self.confidence:
            return text
        else:
            return None

    def text_similar(self, source_text, target_pillow_image):
        """
        检查指定图像中是否包含特定的文字
        :param source_text: 要查找的文字
        :param target_pillow_image: 目标图像，函数将从这个图像提取文字，
        :return:相似度，完全相同是1，完全不同是0，其他是 source_text 与识别出来的文字的比例
        """

        if len(source_text) == 0:
            '''如果source_text是空字符，就认为永远能识别不出来'''
            return 0, None

        cv_image = ActionImage.pil_to_cv(target_pillow_image)
        ActionImage.log_image('target', cv_image, debug=self.debug)
        text_from_image = ActionImage.ocr(cv_image)
        if self.debug:
            print('ocr result: {}'.format(text_from_image))

        if source_text in text_from_image:
            return len(source_text) / len(text_from_image), text_from_image
        else:
            return 0, None
