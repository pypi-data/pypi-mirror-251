
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Log:
    """
    This class is used to log messages in the Orchestrator console.
    Arguments:
        connection: Connection instance to orchestrator.
    Attributes:
        connection: Connection instance to orchestrator.
    Methods:
        debug(log): Debug log.
        trace(log): Trace log.
        info(log): Info log.
        system_exception(error): System exception.
        business_exception(error): Business exception.
    """

    def __init__(self, connection):
        self.connection = connection

    def debug(self, log: str):
        """
        Send debug trace to the robot manager console.
        Arguments:
            log: The log message.
        Returns:
            None
        """

        if self.connection:
            log_type = 'debug'
            self.send(log, log_type=log_type)
        else:
            print(f"{bcolors.OKBLUE}{log}{bcolors.ENDC}")

    def trace(self, log: str):
        """
        Send trace to the robot manager console.
        Arguments:
            log: The log message.
        Returns:
            None
        """
        if self.connection:
            log_type = 'trace'
            self.send(log, log_type=log_type)
        else:
            print(f"{bcolors.OKGREEN}{log}{bcolors.ENDC}")


    def log(self, log: str):
        """
        Send info trace to the robot manager console.
        Arguments:
            log: The log message.
        Returns:
            None
        """
        if self.connection:
            log_type = 'log'
            self.send(log, log_type=log_type)
        else:
            print(f"{bcolors.FAIL}{log}{bcolors.ENDC}")

    def system_exception(self, error: str):
        """
        Send systemException trace to the robot manager console.
        Arguments:
            error: The error message.
        """
        if self.connection:
            log_type = 'syex'
            self.send(error, log_type=log_type)
        else:
            print(f"{bcolors.OKCYAN}{error}{bcolors.ENDC}")

    def business_exception(self, error: str):
        """
        Send businessException trace to orchestrator
        Arguments:
            error: The error message.
        """
        if self.connection:
            log_type = 'byex'
            self.send(error, log_type=log_type)
        else:
            print(f"{bcolors.FAIL}{error}{bcolors.ENDC}")

    def send(self, log: str, log_type: str):
        """
        Async function to send logs to orchestrator
        Arguments:
            log: The log message.
            log_type: The log type.
        Raise:
            OrchestratorConnectionError: If the connection with the orchestrator is not established.
        """
        if not self.connection.debug:
            try:
                self.connection.send_message(log, log_type=log_type)
            except:
                raise Exception("Orchestrator is not connected")
        else:
            print(f'{log_type}: {log}')
