import os
import time

import numpy as np
from cnocr import CnOcr
from cv2 import cv2
import aircv as ac
# 话说网易游戏家也有个aircv，功能类似， 还提供了find_sift方法，使用sift算法查找，以后可以试试
# https://github.com/NetEaseGame/aircv
from autopy.core.data.ScreenRect import ScreenRect
from autopy.objtyping.objtyping import DataObject


class ActionImage:
    cnocr = CnOcr()

    @classmethod
    def pil_to_cv(cls, pil_image):
        img_tmp = pil_image.convert('RGB')
        cv_rgb = np.array(img_tmp)
        return cv2.cvtColor(cv_rgb, cv2.COLOR_RGB2BGR)

    @classmethod
    def load_from_file(cls, image_path):
        return cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)

    @classmethod
    def ocr(cls, cv_image, rect=None):
        if rect is not None:
            cv_image = cv_image[rect.top:rect.bottom, rect.left:rect.right]
        cv_image_gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        img_high_contrast = cls.grayscale_linear_transformation(cv_image_gray, 0, 255)

        res_chars = cls.cnocr.ocr_for_single_line(img_high_contrast)

        if len(res_chars) == 0:
            return ''
        else:
            result = ''.join(list(map(str, res_chars)))

            return result

    @staticmethod
    def grayscale_linear_transformation(img_gray, new_min, new_max):
        if img_gray is None:
            return None
        old_max = img_gray.max()
        old_min = img_gray.min()
        if old_min == old_max:
            return img_gray
        scale_ratio = (new_max - new_min) / (old_max - old_min)
        img_gray_new = (img_gray - old_min) * scale_ratio + new_min
        return img_gray_new.astype(np.uint8)

    @classmethod
    def find_all_template(cls, image_current, image_template, min_confidence):
        match_results = ac.find_all_template(image_current, image_template, min_confidence)
        if match_results is None:
            return None
        res_list = []
        for match_result in match_results:
            res = cls._change_result(match_result)
            res_list.append(res)
        return res_list

    @classmethod
    def find_one_template(cls, image_current, image_template, min_confidence=0.5):
        match_result = ac.find_template(image_current, image_template, min_confidence)
        res = cls._change_result(match_result)
        return res

    @classmethod
    def _change_result(cls, match_result):
        if match_result is None:
            return None
        rect_array = match_result['rectangle']
        res = DataObject()
        res.confidence = match_result['confidence']
        res.rect = ScreenRect(rect_array[0][0], rect_array[3][0], rect_array[0][1], rect_array[3][1])
        return res

    @classmethod
    def log_image(cls, name, image, debug=True):
        if not debug:
            return
        path_root = 'log'
        if not os.path.exists(path_root):
            os.makedirs(path_root)
        timestamp = time.time()
        cv2.imwrite('{}/{}_{}.png'.format(path_root, name, timestamp), image)

