class ActionError:
    @staticmethod
    def trigger(params: tuple):
        (msg) = params
        # print("ERROR: {}".format(msg))
        raise RuntimeError(msg)

    @staticmethod
    def locate_state(params: tuple):
        """
        这个方法的意思，是如果失败了，那么重新查找当前界面处于哪个状态，但是真正的查找逻辑是在Executor中，这里只是输出一下
        :param params:
        :return:
        """
        (msg) = params
        print("ERROR: {}".format(msg))




