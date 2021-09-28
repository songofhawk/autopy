from typing import List, Dict

from .Misc import State
from .ScreenRect import ScreenRect


class Project:
    name: str = None
    ver: int = 0
    screen_width: int
    screen_height: int
    range: ScreenRect = None
    time_scale: float = 1.0
    states: List[State] = []

    def __init__(self):
        self.all_states: Dict[int, State] = {}
        self.path_root = None

