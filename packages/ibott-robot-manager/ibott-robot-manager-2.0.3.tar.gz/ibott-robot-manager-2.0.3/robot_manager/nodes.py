from robot_manager.flow import RobotFlow


class RobotNode:
    """
    This class is used to create a node for the robot.
    :param method: method from the robot class
    :param parent: Parents node
    :param position: Position of the node

    """

    def __init__(self, **kwargs):
        self.method = kwargs.get("method")
        self.position = kwargs.get("position")
        self.parent_nodes = kwargs.get("parents", None)
        self.children = kwargs.get("children")
        self.name = self.method.__name__
        self.exception = None
        self.retry_times = 0
        self.args = None
        self.next_node = None
        self.doc = self.method.__doc__
        self.node_flows = []
        self.data = None


    def connect(self, next_node, pathName=None):
        """
        This method is used to connect the current node to the next node.
        receives the next node and the path name.
        :param next_node:
        :param pathName:
        :return:
        """
        self.next_node = next_node
        if pathName:
            flow_path = f"{str(self.position)}-->|{pathName}|{str(next_node.position)}"
        else:
            flow_path = f"{str(self.position)}-->{str(next_node.position)}"
        self.node_flows.append(flow_path)

    def get_next(self, *args):
        """
        This method is used to run the node.
        """
        return self.next_node


class StartClass(RobotNode):
    """
    This class is used to create a start node.
    :param **kwargs:
    :type **kwargs:
    """

    def __init__(self, **kwargs):
        """Initialize Node Class """
        super().__init__(**kwargs)
        self.node_type = "StartNode"
        self.__name__ = f"{self.method.__name__}({self.node_type})"

        self.node_object = f"{str(self.position)}(({self.name}))"
        if self.position > 0:
            raise ValueError("Start Node must be in first position of the flow")




class ConditionClass(RobotNode):
    """
    ConditionClass is used to create a condition node.
    Heritates from RobotNode Class.

    Arguments:
    =========
    To instance Conditional classes.
        1. function: Function to be used as condition.
        2. parents: *optional - Defines the ancestors of the current node in the flow
        3. condition: *optional - Defines the condition of the current node for conditional nodes

    Methods:
    ========
    Custom methods: override the default implementation of RobotNode class.
        1. Connect: Creates a double connection for node (OnTrueNode/OnFalseNode).
        2. Run: This method is used to run conditional nodes.
           Evaluates function and executes next node (OnTrueNode/OnFalseNode) depending on the result.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.node_type = "ConditionNode"
        self.node_object = str(self.position) + "{" + self.name + "}"
        self.condition = kwargs.get("function")
        self.children = kwargs.get("children")
        self.__name__ = f"{self.method.__name__}({self.node_type})"



    def connect(self, nodes):
        """
        This method is used to connect the current node to the next nodes.
        Evaluating node_types and setting the corresponding onTrueNode and onFalseNode and the flow_path attribute.

        Arguments:
        module: type RobotNode -> module to be connected to the current node.
        """

        try:
            for key in nodes.keys():
                node = RobotFlow.get_node(nodes.get(key))
                flow_path = f"{str(self.position)}-->|{key}|{str(node.position)}"
                self.node_flows.append(flow_path)
        except:
            raise ValueError("Wrong module connection for ConditionClass")

    def get_next(self, *args):
        """
        This method is used to run the conditional nodes.
        Evaluates function and execute the next node (OnTrueNode/OnFalseNode) depending on the result.
        Arguments:
        robot: type Robot -> robot object.
        *args: *optional - Defines the arguments of the current node.
        """
        self.data = args[0]
        return RobotFlow.get_node(self.children.get(self.condition(self.data)))

class OperationClass(RobotNode):
    """
    This class is used to create an operation node.
    Heritates from RobotNode Class
    :param **kwargs:
    :type **kwargs:
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.node_type = "OperationNode"
        self.__name__ = f"{self.method.__name__}({self.node_type})"
        self.node_object = f"{str(self.position)}[{self.name}]"


class EndClass(RobotNode):
    """
    This class is used to create an end node.
    Heritates from RobotNode Class
    :param **kwargs:
    :type **kwargs:
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.node_type = "EndNode"
        self.node_object = f"{str(self.position)}([{self.name}])"

    def connect(self, **kwargs):
        """
        This method is used to connect the current node to the next node.
        :param kwargs:

        raises ValueError if the node is not in the last position of the flow
        """
        raise ValueError("EndNode Must be at the end of the flow")

    def get_next(self, *args):
        return False