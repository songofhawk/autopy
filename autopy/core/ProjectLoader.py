import inspect
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


def has_init_argument(clazz):
    signature = inspect.signature(clazz.__init__)
    for name, parameter in signature.parameters.items():
        # print(clazz.__name__, name, parameter.default, parameter.annotation, parameter.kind)
        if name not in ['self', 'args', 'kwargs']:
            return True
    return False


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
        if has_init_argument(clazz):
            raise TypeError('类 {} 的构造函数需要参数，无法通过CommentedMap实例化！\r\n {}'.format(clazz.__name__, yaml_obj))
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
        if hasattr(clazz, '__origin__'):
            # __origin__ 是泛型对应的原始类型，比如list或是dict
            generic_type = clazz.__args__[0]
            # __args__ 是泛型参数数组，对于list来说，它只有一个元素，表示了list中保存的是什么类型的数据，如果是dict，它应该有两个参数，分别表示key和value的数据类型
            # 这里获取了list中应当保存的数据类型
        else:
            # 之前考虑预期类型应该和实际类型匹配，也就是'class.__origin__ is list'，
            # 但为了更灵活一些，有些节点是既可以是类实例，也可以是该实例组成的数组的，比如check节点
            # 所以改成了即使预期定义不是list，这里也按list解析
            generic_type = clazz

        for item in yaml_obj:
            obj = yaml_to_typed_obj(item, generic_type)
            new_list.append(obj)
        return new_list

    elif isinstance(yaml_obj, str):
        if clazz is str:
            # 如果预期类型和实例类型相同，直接返回
            return yaml_obj
        elif clazz is int or clazz is float:
            # 如果预期类型和实例类型不同，但都是基础类型，尝试强制类型转换
            return str(yaml_obj)
        else:
            # 如果预期类型和实例类型不同，并且预期类型是个class，尝试调用构造函数创建实例
            return clazz(yaml_obj)
    elif isinstance(yaml_obj, int):
        if clazz is int:
            # 如果预期类型和实例类型相同，直接返回
            return yaml_obj
        elif clazz is str or clazz is float:
            # 如果预期类型和实例类型不同，但都是基础类型，尝试强制类型转换
            return int(yaml_obj)
        else:
            return clazz(yaml_obj)
    elif isinstance(yaml_obj, float):
        if clazz is float:
            # 如果预期类型和实例类型相同，直接返回
            return yaml_obj
        elif clazz is int or clazz is str:
            # 如果预期类型和实例类型不同，但都是基础类型，尝试强制类型转换
            return float(yaml_obj)
        else:
            # 如果预期类型和实例类型不同，并且预期类型是个class，尝试调用构造函数创建实例
            return clazz(yaml_obj)
    else:
        # raise TypeError('需要转换的对象，是一个出乎意料的类型：{}，\n\r{}'.format(type(yaml_obj), yaml_obj))
        # 对于实现了from_yaml的类，可以直接得到对象实例
        return yaml_obj
