from autopy.core.Project import Project


class Executor:
    project: Project = None

    def __init__(self, project: Project):
        self.project = Project