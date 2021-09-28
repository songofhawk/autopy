import time

from autopy.core.Variable import Variable
from autopy.core.action.ActionScreen import ActionScreen
from autopy.core.const import STATE, FIND_RESULT
from autopy.core.data.Action import Action
from autopy.core.data.Misc import Find
from autopy.core.data.Misc import ForEach
from autopy.core.data.Project import Project


class Env(object):
    @classmethod
    def adjust_resolution(cls, screen_width, screen_height):
        ActionScreen.change_resolution((screen_width, screen_height))


class Executor:
    project: Project = None
    variables: Variable = Variable()

    def __init__(self, project: Project):
        self.project = project
        self._current_state = None
        self._current_index = None
        self._current_states = None

        # 用列表实现栈
        self._currents = []

    def run(self):
        if self.project is None:
            return

        self._load_env()
        states = self.project.states
        if states is None or len(states) == 0:
            return
        self._current_states = states
        init_state = states[0]
        self._current_index = 0
        self._current_state = init_state
        while self._current_state is not None:
            self._one_state(self._current_state)

    def _load_env(self):
        if self.project.screen_width is not None and \
                self.project.screen_height is not None:
            Env.adjust_resolution(self.project.screen_width, self.project.screen_height)

    # def _run_from_state(self, init_state):
    #     self._one_state(init_state)

    def _one_state(self, the_state):
        print('enter state "{}"'.format(the_state.name))
        Action.save_call_env({STATE: the_state})

        if not self._do_check(the_state.check):
            return

        self._call_action(the_state.action)

        self._do_find(the_state.find)

        foreach = the_state.foreach
        if isinstance(foreach, ForEach):
            foreach.do(self)

        '''从这里开始，处理transition模块'''
        transition = the_state.transition
        if transition is None:
            print('reach the end state!')
            self._current_state = None
            self._current_index = None
            return
        if transition.reach_max_time():
            print('reach max time({}) of transition, terminate!'.format(transition.max_time))
            self._current_state = None
            self._current_index = None
            return

        if transition.wait_before is not None:
            time.sleep(transition.wait_before)

        # 首先调用触发transition的动作
        self._call_action(transition.action)

        if transition.wait is not None:
            time.sleep(transition.wait)

        # 如果有子状态集，进入首选子状态
        sub_states = transition.sub_states
        if sub_states is not None and len(sub_states) > 0:
            self.drill_into_substates(sub_states)

        # 迁移到下一个状态
        transition.count()
        trans_to = transition.to
        next_state, next_index = self._get_next_state(trans_to)
        if next_state is None:
            self._current_state = None
            self._current_index = None
            return

        self._current_index = next_index
        self._current_state = next_state

    @staticmethod
    def _call_action(action):
        if action is None:
            return
        if isinstance(action, Action):
            action.call()
        elif isinstance(action, list):
            for one_action in action:
                one_action.call()

    def drill_into_substates(self, sub_states):
        self.push_currents()

        self._current_index = 0
        sub_init_state = sub_states[0]
        self._current_states = sub_states
        self._current_state = sub_init_state
        while self._current_state is not None:
            self._one_state(self._current_state)

        self.pop_currents()

    def _get_next_state(self, trans_to):
        if trans_to.is_next:
            if self._current_index < len(self._current_states) - 1:
                next_index = self._current_index + 1
                next_state = self._current_states[next_index]
            else:
                next_state = None
                next_index = None
        elif trans_to.id is not None:
            next_state, next_index = self._find_state_by_id(self._current_states, trans_to.id)
        else:
            next_state = None
            next_index = None
        return next_state, next_index

    @staticmethod
    def _find_state_by_id(current_states, state_id):
        for i, state in enumerate(current_states):
            if state.id == state_id:
                return state, i
        return None, None

    def push_currents(self):
        self._currents.append((self._current_state, self._current_index, self._current_states))

    def pop_currents(self):
        (self._current_state, self._current_index, self._current_states) = self._currents.pop()

    def _do_check(self, check):
        """
        check的目标是检查页面是否中的处于当前状态，所以只要有一条不符，就失败。此时如果fail_action是locate_state，就会从当前状态组中逐一检查处于哪个状态，并且直接跳转到对应的状态执行
        :param check:
        :return:
        """
        check_pass, fail_action = self._get_check_result(check, True)
        if check_pass:
            return True

        if fail_action is not None and fail_action.is_locate_state:
            print("即将定位当前界面处于那个状态...")
            for one_state in self._current_states[::-1]:
                # 逆序遍历状态列表,也可以用reversed方法
                print("-- 测试是否属于状态'{}'".format(one_state.name))
                locate_check = one_state.check
                if locate_check is None:
                    continue
                check_pass, _ = self._get_check_result(locate_check, False)
                if check_pass:
                    print("---- 找到了,就是这个状态!")
                    self._current_state = one_state
                    self._current_index = one_state.id
                    return False
            self._current_state = None
            self._current_index = None
            return False
        else:
            self._current_state = None
            self._current_index = None
            return False

    @staticmethod
    def _get_check_result(check, exe_fail_action):
        """
        check和find的区别在于, 如果有多条, check是只要其中一条不满足, 就退出
        :param check:
        :return check_pass: 检查是否通过
        :return fail_action: 如果没通过,对应的fail_action
        """
        if check is None:
            return True, None

        fail_action = None
        if isinstance(check, list):
            check_pass = True
            for check_one in check:
                result_one = check_one.do(exe_fail_action)
                if result_one is None:
                    check_pass = False
                    fail_action = check_one.fail_action
                    break
        elif isinstance(check, Find):
            result_one = check.do(exe_fail_action)
            if result_one is None:
                check_pass = False
                fail_action = check.fail_action
            else:
                check_pass = True
        else:
            raise RuntimeError("Expect a Find object in checking, but got a {}".format(type(check)))
        return check_pass, fail_action

    @staticmethod
    def _do_find(find):
        """
        find的目标是为迁移到下一个状态做准备, 所以如果有多条，那么就逐一收集查找结果
        :param find: 待执行的查找对象
        :return: 查找结果
        """
        if find is None:
            return None

        if isinstance(find, list):
            found = []
            for find_one in find:
                find_result = find_one.do()
                if find_result is not None:
                    found.append(find_result)
            if len(found) == 0:
                found = None
        elif isinstance(find, Find):
            found = find.do()
        else:
            raise RuntimeError("Expect a Find object in finding, but got a {}".format(type(find)))

        Action.save_call_env({FIND_RESULT: found})
        return found
