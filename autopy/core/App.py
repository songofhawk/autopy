from autopy.core import Option
from autopy.core.Executor import Executor
from autopy.core.Project import Project


class App:
    option: Option = None
    project: Project = None

    def __init__(self, option: Option):
        self.option = option
        self.load_project(option.project)

    def load_project(self, project_file: str):
        self.project = ProjectLoader.load(project_file)

    def execute(self):
        executor = Executor(self.option.project)
