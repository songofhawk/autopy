from typing import List

from .ScreenRect import ScreenRect
from .State import State


class Project:
    name: str = None
    ver: int = 0
    screen_with: int = 1920
    screen_height: int = 1080
    range: ScreenRect = None
    states: List[State] = []
