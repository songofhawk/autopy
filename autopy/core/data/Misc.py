from __future__ import annotations

from typing import List

from autopy.core.data.Action import Action, Execution, Evaluation
from autopy.core.data.Find import Find


class To:
    def __init__(self, _to='next'):
        self.is_next = False
        self.id = None
        self._to = _to
        self.parse()

    def parse(self):
        _to = self._to
        if _to == 'next':
            self.is_next = True
            return
        else:
            self.is_next = False
        if isinstance(_to, int):
            self.id = _to
        elif _to.isdigit():
            self.id = int(self._to)


class Transition:
    action: Execution
    wait_before: int
    wait: int
    to: To
    sub_states: List[State]
    max_time: int

    def __init__(self):
        self._trans_time = 0

    def count(self):
        self._trans_time += 1

    def reach_max_time(self):
        return False if self.max_time is None else self._trans_time >= self.max_time


class State:
    name: str = None
    id: int = -1
    check: Find
    find: Find
    action: Execution
    transition: Transition
    foreach: ForEach


class ForEach:
    in_items: Evaluation
    item: str
    action: Execution
    sub_states: List[State]

    def __init__(self):
        self.call_env = {}

    def do(self, executor):
        items = self.in_items.call()
        item_name = 'item' if self.item is None else self.item
        if isinstance(items, list):
            for item in items:
                self.call_env[item_name] = item
                self._do_one(executor)
        else:
            self.call_env[item_name] = items
            self._do_one(executor)

    def _do_one(self, executor):
        if isinstance(self.action, Action):
            self.action.call(self.call_env)
        elif isinstance(self.action, list):
            for one_action in self.action:
                one_action.call(self.call_env)

        sub_states = self.sub_states
        if sub_states is not None and len(sub_states) > 0:
            executor.drill_into_substates(sub_states)

