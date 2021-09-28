import pyautogui


class ActionKeyboard:
    @staticmethod
    def hotkey(*keys):
        pyautogui.hotkey(*keys)

    @staticmethod
    def type(str_to_type, interval=0):
        if interval == 0:
            pyautogui.write(str_to_type)
        else:
            pyautogui.write(str_to_type, interval)

    @staticmethod
    def press(key_or_keys, interval=0):
        if interval == 0:
            pyautogui.press(key_or_keys)
        else:
            pyautogui.press(key_or_keys, interval)
