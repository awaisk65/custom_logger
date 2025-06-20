from logging_config import setup_logging
import logging
from class1 import Class1

class Helloooooo:
    def __init__(self):
        # setup_logging()  # Configure it once, globally
        setup_logging(self.__class__.__name__)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.class1 = Class1()
        self.logger.info("Class2 initialized")
        self.logger.debug("Debug msg")
        self.logger.warning("warning msg")
        self.logger.error("error msg")

obj = Helloooooo()