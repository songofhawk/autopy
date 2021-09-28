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
    def __init__(self, action_str):
        super().__init__(action_str)
        self.exp = compile(action_str, '', 'eval')

    def evaluate_exp(self):
        super()._prepare_exp()
        return eval(self.exp, {"__builtins__": {}}, Action._call_env)


class Execution(Action):
    def __init__(self, action_str):
        super().__init__(action_str)
        self.exp = compile(action_str, '', 'exec')

    def evaluate_exp(self):
        super()._prepare_exp()
        return exec(self.exp, {"__builtins__": {}}, Action._call_env)
