import typing

from autopy.core.data import Project
from autopy.core.lib.yaml import yaml
from autopy.core.data.Project import Project
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from typing import get_type_hints


class ProjectLoader:
    @classmethod
    def load(cls, project_file):
        with open(project_file, encoding='utf-8') as f:
            yaml_obj = yaml.load(f)
            project = yaml_to_typed_obj(yaml_obj, Project)
            # for k, v in project_map.items():
            #     cls.handle_value(project, k, v)
            return project


def yaml_to_typed_obj(yaml_obj, clazz):
    '''

    :param yaml_obj:
    :param clazz:
    :return:
    注意: 这里跟generic泛型相关的一些判断，比如__origin__, __args__都是低于python3.7版本的，更高版本还有待完善
    参考：
    * https://stackoverflow.com/questions/49171189/whats-the-correct-way-to-check-if-an-object-is-a-typing-generic
    * https://mypy.readthedocs.io/en/stable/kinds_of_types.html
    * https://docs.python.org/zh-cn/3/library/typing.html
    '''
    if isinstance(yaml_obj, CommentedMap):
        obj = clazz()
        for k, v in yaml_obj.items():
            types = get_type_hints(clazz)
            if k not in types:
                continue
            type_hint = types[k]
            setattr(obj, k, yaml_to_typed_obj(v, type_hint))
        return obj
    elif isinstance(yaml_obj, CommentedSeq):
        new_list = []
        if clazz.__origin__ is not list:
            # __origin__ 是泛型对应的原始类型，比如list或是dict
            # 在这里因为yaml对象是个list，它对应的类型应该也是个list，要不就无法匹配了
            raise TypeError('需要转换的对象，应该是一个列表，但它的定义是：{}\n\r'.format(clazz, yaml_obj))

        generic_type = clazz.__args__[0]
        # __args__ 是泛型参数数组，对于list来说，它只有一个元素，表示了list中保存的是什么类型的数据，如果是dict，它应该有两个参数，分别表示key和value的数据类型
        # 这里获取了list中应当保存的数据类型
        for item in yaml_obj:
            obj = yaml_to_typed_obj(item, generic_type)
            new_list.append(obj)
        return new_list

    else:
        return yaml_obj
