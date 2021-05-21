import inspect
from typing import get_type_hints

from ruamel.yaml.comments import CommentedMap, CommentedSeq

from autopy.core.data import Project
from autopy.core.data.DataObject import DataObject
from autopy.core.data.Project import Project
from autopy.core.lib.yaml import yaml


class ProjectLoader:
    @classmethod
    def load(cls, project_file):
        with open(project_file, encoding='utf-8') as f:
            yaml_obj = yaml.load(f)
            project = yaml_to_typed_obj(yaml_obj, Project)
            # project.states[0].transition.to.state = None
            # project_clean = yaml_to_typed_obj(yaml_obj, Project, reserve_extra_attr=False)
            return project


def get_type_definition(obj):
    types_in_class = get_type_hints(type(obj))
    instance_in_obj = obj.__dict__
    for k, v in instance_in_obj.items():
        types_in_class[k] = type(v)

    # 这里有个合并两个字典的方法，要求python >= 3.5
    # types = {**types_in_class, **types_in_obj}
    return types_in_class


def has_init_argument(clazz):
    signature = inspect.signature(clazz.__init__)
    for name, parameter in signature.parameters.items():
        # print(clazz.__name__, name, parameter.default, parameter.annotation, parameter.kind)
        if name not in ['self', 'args', 'kwargs']:
            return True
    return False


def yaml_to_typed_obj(yaml_obj, clazz, reserve_extra_attr=True, init_empty_attr=True):
    """
    把CommentedMap-CommentedSeq结构的yaml对象（树状结构），转换为预定义好类型的类实例，
    本函数是个递归函数，将按深度优先遍历yaml树的所有节点，并逐级对应到clazz指定的类属性中
    :param yaml_obj: yaml对象
    :param clazz: 类定义，表示要实例化的对象类型，
                    当这个参数的值为None，那么就根据reserve_extra_attr参数判断:
                    如果reserve_extra_attr=True，就把参数yaml_obj转换为普通的dict-list树状结构
                    如果reserve_extra_attr=False，就忽略这个对象
    :param reserve_extra_attr: 是否保留那些在clazz中未定义，但yaml_obj中存在的属性；
        缺省为True，也就是即使clazz中未定义，也设置为对象的属性，如果不是基本类型，那就就装换为DataObject类
        如果为False，那就就严格按照clazz的定义转换，忽略所有未定义的属性
    :param init_empty_attr: 是否初始化yaml_obj中没有的属性（但是clazz定义中有）
        如果为True，那么把yaml_obj中没有的属性都初始化为None
        如果为False，那么什么都不做，结果就是生成的对象中根本没有这个属性
    :return:
    注意: 这里跟generic泛型相关的一些判断，比如__origin__, __args__都是低于python3.7版本的，更高版本还有待完善
    参考：
    * https://stackoverflow.com/questions/49171189/whats-the-correct-way-to-check-if-an-object-is-a-typing-generic
    * https://mypy.readthedocs.io/en/stable/kinds_of_types.html
    * https://docs.python.org/zh-cn/3/library/typing.html
    * https://sikasjc.github.io/2018/07/14/type-hint-in-python/
    """
    if clazz is None and not reserve_extra_attr:
        return None

    if isinstance(yaml_obj, CommentedSeq):
        new_list = []
        if clazz is None:
            item_type = None
        elif hasattr(clazz, '__origin__'):
            # __origin__ 是泛型对应的原始类型，比如list或是dict
            item_type = clazz.__args__[0]
            # __args__ 是泛型参数数组，对于list来说，它只有一个元素，表示了list中保存的是什么类型的数据，如果是dict，它应该有两个参数，分别表示key和value的数据类型
            # 这里获取了list中应当保存的数据类型
        else:
            # 之前考虑预期类型应该和实际类型匹配，也就是'class.__origin__ is list'，
            # 但为了更灵活一些，有些节点是既可以是类实例，也可以是该实例组成的数组的，比如check节点
            # 所以改成了即使预期定义不是list，这里也按list解析
            item_type = clazz

        for item in yaml_obj:
            typed_obj = yaml_to_typed_obj(item, item_type, reserve_extra_attr, init_empty_attr)
            if typed_obj is not None:
                new_list.append(typed_obj)
        return new_list

    elif isinstance(yaml_obj, CommentedMap):
        if has_init_argument(clazz):
            raise TypeError('类 {} 的构造函数需要参数，无法通过CommentedMap实例化！\r\n {}'.format(clazz.__name__, yaml_obj))
        if clazz is None:
            obj = DataObject()
            types = None
        else:
            obj = clazz()
            types = get_type_definition(obj)

        for k, v in yaml_obj.items():
            if types is not None and k in types:
                attr_type = types[k]
            else:
                attr_type = None
            typed_obj = yaml_to_typed_obj(v, attr_type, reserve_extra_attr, init_empty_attr)
            if typed_obj is not None:
                setattr(obj, k, typed_obj)

        if init_empty_attr:
            for k in types.keys():
                if k not in yaml_obj:
                    setattr(obj, k, None)

        return obj
    elif isinstance(yaml_obj, str):
        if clazz is None:
            return yaml_obj
        elif clazz is str:
            # 如果预期类型和实例类型相同，直接返回
            return yaml_obj
        elif clazz is int or clazz is float:
            # 如果预期类型和实例类型不同，但都是基础类型，尝试强制类型转换
            return str(yaml_obj)
        else:
            # 如果预期类型和实例类型不同，并且预期类型是个class，尝试调用构造函数创建实例
            return clazz(yaml_obj)
    elif isinstance(yaml_obj, int):
        if clazz is None:
            return yaml_obj
        elif clazz is int:
            # 如果预期类型和实例类型相同，直接返回
            return yaml_obj
        elif clazz is str or clazz is float:
            # 如果预期类型和实例类型不同，但都是基础类型，尝试强制类型转换
            return int(yaml_obj)
        else:
            return clazz(yaml_obj)
    elif isinstance(yaml_obj, float):
        if clazz is None:
            return yaml_obj
        elif clazz is float:
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
