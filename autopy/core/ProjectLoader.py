from autopy.core.data import Project
from autopy.core.lib.yaml import yaml
from autopy.core.data.Project import Project
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from typing import get_type_hints


class ProjectLoader:
    @classmethod
    def load(cls, project_file):
        project = Project()
        all = dir(project)

        with open(project_file, encoding='utf-8') as f:
            project_map = yaml.load(f)
            for k, v in project_map.items():
                cls.handle_value(project, k, v)
        return project

    @classmethod
    def handle_value(cls, obj, key: str, value):
        if isinstance(value, CommentedSeq):
            """
            这里覆盖了父类针对dict和list类型的判断，改为针对CommentedMap和CommentedSeq
            """
            new_list = []
            for item in value:
                if isinstance(item, CommentedMap):
                    new_list.append(cls(item))
                else:
                    new_list.append(item)
            setattr(obj, key, new_list)

        elif isinstance(value, CommentedMap):
            setattr(obj, key, cls(value))
        else:
            setattr(obj, key, value)
