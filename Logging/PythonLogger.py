import logging

from Config.python_logger_config import PYTHON_LOGGER_NAME
from Logging.ILogger import ILogger


class PythonLogger(ILogger):
    def __init__(self, output_file=None, level=logging.INFO):
        logging.basicConfig(filename=output_file, level=level)
        self.logger = logging.getLogger(PYTHON_LOGGER_NAME)

    def log(self, message):
        self.logger.info(message)

    def session_log(self, func):
        def wrapper(*args, **kwargs):
            self.log("Session started!")
            func(*args, **kwargs)
            self.log("Session ended!")

        return wrapper
