import time

from autopy.core.action import ActionMouse
from autopy.core.action.ActionClipboard import ActionClipboard
from autopy.core.action.ActionError import ActionError
from autopy.core.action.ActionImage import ActionImage
from autopy.core.action.ActionKeyboard import ActionKeyboard
from autopy.core.action.ActionScreen import ActionScreen
from autopy.core.action.ActionWindow import ActionWindow
from autopy.core.const import MOUSE
from autopy.core.data.ScreenRect import ScreenRect


class Action:
    """
    执行操作基础类，有Evaluation和Execution两个子类，分别对应有返回结果和没有返回结果的操作。在本基础类中，还定义了所有具体的操作方法名，这些方法可以在Action类型的配置节点中直接调用。具体的参数会在对应的类中介绍

    Attributes:
        move (ActionMouse.move) : 移动鼠标
        raise_error  (ActionError.trigger) : 引发异常
        click  (ActionMouse.click) : 点击鼠标
        dbclick  (ActionMouse.dbclick) : 双击鼠标
        rightclick  (ActionMouse.rightclick) : 右键点击鼠标
        hotkey  (ActionKeyboard.hotkey) : 点击键盘热键
        type  (ActionKeyboard.type) : 输入字符串（模拟键盘输入，参数是整个字符串）
        press  (ActionKeyboard.press) : 点击键盘（指定一个键）
        ocr  (ActionImage.ocr) : 识别给定图片中的文字
        print  (print) : 打印信息到控制台
        find_template  (ActionImage.find_one_template) : 在指定图像中，查找另外一幅图像
        snapshot  (ActionScreen.snapshot_cv) : 屏幕截图
        log_image  (ActionImage.log_image) : 保存图片到文件
        ScreenRect  (ScreenRect) : 新建一个ScreenRect对象
        wait  (time.sleep) : 等待指定时间（秒）
        copy  (ActionClipboard.copy) : 复制
        paste  (ActionClipboard.paste) : 粘贴
        locate_state  (ActionError.locate_state) : 定位当前处于哪个State
        set_window_pos  (ActionWindow.set_window_pos) : 设置窗口的位置和大小

    """
    func_dict = {
        'move': ActionMouse.move,
        'raise_error': ActionError.trigger,
        'click': ActionMouse.click,
        'dbclick': ActionMouse.dbclick,
        'rightclick': ActionMouse.rightclick,
        'hotkey': ActionKeyboard.hotkey,
        'type': ActionKeyboard.type,
        'press': ActionKeyboard.press,
        'ocr': ActionImage.ocr,
        'print': print,
        'find_template': ActionImage.find_one_template,
        'snapshot': ActionScreen.snapshot_cv,
        'log_image': ActionImage.log_image,
        'ScreenRect': ScreenRect,
        'wait': time.sleep,
        'copy': ActionClipboard.copy,
        'paste': ActionClipboard.paste,
        'locate_state': ActionError.locate_state,
        'set_window_pos': ActionWindow.set_window_pos,
    }

    _call_env = {**func_dict, **{}}

    def __init__(self, action_str):
        self._action_str = action_str
        if action_str.startswith('locate_state'):
            self.is_locate_state = True

    def call(self, call_env=None):
        if call_env is not None:
            if isinstance(call_env, dict):
                self.save_call_env(call_env)
            else:
                raise RuntimeError('The argument in "call" method of "Action" object, should be a dict, but {} is passed'.format(type(call_env)))
        return self.evaluate_exp()

    def evaluate_exp(self):
        raise RuntimeError('_evaluate_exp is an abstract method, can not be called in an Action object!')

    def _prepare_exp(self):
        self._call_env[MOUSE] = ActionMouse.position()

    @classmethod
    def save_call_env(cls, call_env):
        cls._call_env.update(call_env)

    @classmethod
    def get_call_env(cls, name):
        return cls._call_env[name]


class Evaluation(Action):
    """
    Action操作类的子类，执行以后会有返回值
    """
    def __init__(self, action_str):
        super().__init__(action_str)
        self.exp = compile(action_str, '', 'eval')

    def evaluate_exp(self):
        super()._prepare_exp()
        return eval(self.exp, {"__builtins__": {}}, Action._call_env)


class Execution(Action):
    """
    Action操作类的子类，执行以后没有返回值
    """
    def __init__(self, action_str):
        super().__init__(action_str)
        self.exp = compile(action_str, '', 'exec')

    def evaluate_exp(self):
        super()._prepare_exp()
        return exec(self.exp, {"__builtins__": {}}, Action._call_env)
