from autopy.core.Option import Option
from autopy.core.ProjectLoader import ProjectLoader
from autopy.core.Executor import Executor
from autopy.core.data.Project import Project


class App:
    option: Option = None
    project: Project = None

    def __init__(self, option: Option):
        self.option = option
        self.load_project(option.project)

    def load_project(self, project_file: str):
        self.project = ProjectLoader.load(project_file)

    def execute(self):
        executor = Executor(self.project)
        executor.run()
