import pyperclip


class ActionClipboard:
    @classmethod
    def copy(cls, str_to_copy):
        pyperclip.copy(str_to_copy)

    @classmethod
    def paste(cls):
        pyperclip.paste()
