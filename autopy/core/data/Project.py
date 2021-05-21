from typing import List

from .ScreenRect import ScreenRect
from .State import State, Find


class Project:
    name: str = None
    ver: int = 0
    screen_width: int = 1920
    screen_height: int = 1080
    range: ScreenRect = None
    time_scale: float = 1.0
    states: List[State] = []

    def __init__(self):
        self.sub_states: List[State] = []
