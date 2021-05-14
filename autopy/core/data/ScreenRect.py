from autopy.core.lib.yaml import yaml
from ruamel.yaml import yaml_object
from operator import methodcaller


@yaml_object(yaml)
class ScreenRect(dict):
    yaml_tag = u'!rect'

    # screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    # screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    def __init__(self, left: int = None, right: int = None, top: int = None, bottom: int = None):
        # super(ScreenRect, self).__init__([left, right, top, bottom])
        # self._inner_list = [left, right, top, bottom]
        self['l'] = left
        self['r'] = right
        self['t'] = top
        self['b'] = bottom

    @property
    def left(self):
        return self['l']

    @property
    def right(self):
        return self['r']

    @property
    def top(self):
        return self['t']

    @property
    def bottom(self):
        return self['b']

    def swap_top_bottom(self):
        temp_top = self.top
        top = self.screen_height - temp_top if temp_top < self.screen_height else 0
        bottom = self.screen_height - self.bottom if self.bottom < self.screen_height else 0
        return ScreenRect(self.left, self.right, top, bottom)

    def __str__(self):
        return 'l:{},  r:{},  t:{},  b:{}'.format(self.left, self.right, self.top, self.bottom)

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag,
                                            'l:{}, r:{}, t:{}, b:{}'.format(node.left, node.right, node.top,
                                                                            node.bottom))
        # return {'l': self.left, 'r': self.right, 't': self.top, 'b': self.bottom}

    @classmethod
    def from_yaml(cls, constructor, node):
        splits = node.value.split(', ')
        # test = list(map(lambda x: x + '_sss', splits))
        v = list(map(lambda x: x[1], map(methodcaller("split", ":"), splits)))
        # print(v)
        return cls(left=int(v[0]), right=int(v[1]), top=int(v[2]), bottom=int(v[3]))
