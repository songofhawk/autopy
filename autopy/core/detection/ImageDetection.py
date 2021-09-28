import PIL

from autopy.core.action.ActionImage import ActionImage
from autopy.core.action.ActionScreen import ActionScreen
from autopy.core.data import Action
from autopy.core.data.ScreenRect import ScreenRect
from autopy.core.detection.Detection import Detection


class ImageDetection(Detection):
    snapshot: ScreenRect
    confidence: float = 0.8
    keep_clip: Action.Evaluation

    def do(self, find_all=False):
        snapshot_image = ActionScreen.snapshot(self.snapshot.evaluate())
        screen_image = ActionImage.pil_to_cv(snapshot_image)
        res = self.image_in(self._get_template_full_path(), screen_image, self.confidence, find_all)
        if res is None:
            return None
        if isinstance(res, list):
            new_res = []
            for one in res:
                one.rect_on_image = one.rect
                one.rect_on_screen = one.rect.offset_by(self.snapshot)
                one.image = screen_image
                self.get_clip(one)
                new_res.append(one)
            return new_res
        else:
            res.rect_on_image = res.rect
            res.rect_on_screen = res.rect.offset_by(self.snapshot)
            res.image = screen_image
            self.get_clip(res)
            return res  # rect是相对偏移量

    def image_in(self, template_file_path, big_image, min_confidence, find_all):
        """
        检查两幅图是否相似
        :param min_confidence: 最低可信度, 不足这个可信度的结果将被忽略
        :param find_all: 是否查找所有结果,如果为False, 那么只返回第一个
        :param template_file_path: 要查找的图文件路径位置
        :param big_image: 大图
        :return:相似度，完全相同是1，完全不同是0
        目标图像需要是pillow格式的，将在函数中被转换为opencv格式的，最后用aircv的find_template方法比较是否相似
        """
        if isinstance(big_image, PIL.Image.Image):
            image_current = ActionImage.pil_to_cv(big_image)
        else:
            image_current = big_image

        ActionImage.log_image('current', image_current, debug=self.debug)
        image_template = ActionImage.load_from_file(template_file_path)
        ActionImage.log_image('template', image_template, debug=self.debug)

        if find_all:
            result_list = ActionImage.find_all_template(image_current, image_template, min_confidence)
            # if self.debug:
            #     for result in result_list:
            #         rect = result.rect
            #         self.log_image('match', image_current[rect.top:rect.bottom, rect.left:rect.right])
            return result_list
        else:
            result = ActionImage.find_one_template(image_current, image_template, min_confidence)
            if self.debug:
                print('image detection result: {}, {}'.format(result.confidence if result is not None else None, result.rect if result is not None else None))
            return result

    def get_clip(self, res):
        if self.keep_clip is None:
            return None
        call_env: dict = {'result': res}
        rect = self.keep_clip.call(call_env)
        image = res.image
        clip = image[rect.top:rect.bottom, rect.left:rect.right]

        res.clip = clip
        res.clip_on_image = rect
        res.clip_on_screen = res.clip_on_image.offset_by(self.snapshot)

        return clip
