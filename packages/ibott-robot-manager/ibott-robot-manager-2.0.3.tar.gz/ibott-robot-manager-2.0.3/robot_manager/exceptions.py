import inspect
import traceback
from .flow import RobotFlow


class RobotBaseException(Exception):
    def __init__(self, robot):
        self.robot = robot
        self.traceback = traceback.format_exc()
        self.send_exception()

    def send_exception(self):
        """send exception to orchestrator"""
        for line in self.traceback.splitlines():
            self.robot.log.system_exception(str(line))
        self.robot.log.system_exception("[Execution Failed]")


class RobotException(Exception):
    exceptions = []

    def __init__(self, *args, **kwargs):
        self.__class__.exceptions.append(self)
        frame= inspect.currentframe()
        while frame.f_code.co_name == "__init__":
            frame = frame.f_back
            current_method_name = frame.f_code.co_name
        # get the name of the caller method
        self.robot = args[0]
        self.nodes = RobotFlow.nodes
        self.node = self.robot.node
        #RobotFlow.get_node(current_method_name))
        self.node.exception = self
        self.message = kwargs.get("message", None)
        self.next_action = kwargs.get("next_action", None)
        Exception.__init__(self, self.message)


    def process_exception(self):
        return

    def get_next_node(self, next_method: str):
        """
        get next node from the flow based on the next_method name (string)
        Arguments:
            next_method {string} -- name of the next method
        """
        for node in self.nodes:
            if node.name == next_method:
                return node

    def retry(self, max_retry_times):
        """
        retry the current node
        Arguments:
            max_retry_times {int} -- max retry times
        """

        if self.node.retry_times <= max_retry_times:
            self.robot.node = self.node
            self.node.retry_times = self.node.retry_times + 1
            self.node.exception = None
        else:
            raise RecursionError(f"Max retry times reached for node: {self.node.name}")

    def go_to_node(self, next_node, *args, max_retry_times=None):
        """
        go to the next node   Arguments:
        next_node {function} -- method to be executed when Exception is raised
        max_retry_times {int} -- max retry times
        """
        if max_retry_times == None:
            self.robot.node = RobotFlow.get_node(next_node)
            self.robot.node.args = args
            self.node.exception = None
        elif self.node.retry_times <= max_retry_times:
            self.robot.node = RobotFlow.get_node(next_node)
            self.robot.node.args = args
            self.node.retry_times = self.node.retry_times + 1
            self.node.exception = None
        else:
            raise RecursionError(f"Max retry times reached for node: {self.node.name}")


    def restart(self, max_retry_times):
        """
        Restart process from the beginning of the flow
        Arguments:
            max_retry_times {int} -- max retry times
        """
        if self.node.retry_times <= max_retry_times:
            self.robot.node = self.nodes[0]
            self.node.retry_times += 1
            self.node.exception = None
        else:
            raise RecursionError(f"Max retry times reached for node: {self.node.name}")

    def skip(self):
        """
        skip the current node
        """
        args = self.robot.node.args
        if args is not None:
            self.robot.node = self.node.get_next(args)
        else:
            self.robot.node = self.node.get_next()
        self.node.exception = None

    def stop(self):
        """
        stop the current node
        """
        self.robot.node = self.nodes[-1]
        self.node.exception = None


    @staticmethod
    def count_retry_times(counter=[0]):
        """
        count the retry times of the current node
        Arguments:
            counter {list} -- counter list
        """
        #counter[0] += 1
        #return counter[0]
        self.node.retry_times +=1
