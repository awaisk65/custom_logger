import logging
import logging.config
import os
from datetime import datetime

class CustomLogger(logging.Logger):
    def __init__(self, name, level=logging.DEBUG):
        super().__init__(name, level)
        self.logged_messages = set()

    def _log_once(self, level, msg, *args, **kwargs):
        once = kwargs.pop('once', False)
        if once:
            if msg in self.logged_messages:
                return
            self.logged_messages.add(msg)
        super().log(level, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._log_once(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log_once(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log_once(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._log_once(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._log_once(logging.CRITICAL, msg, *args, **kwargs)

def setup_logging(class_name: str, default_level=logging.DEBUG):
    """
    Set up logging with a unique filename per class caller and global configuration.
    
    Parameters
    ----------
    class_name : str
        Name of the class calling the logger setup.
    default_level : int
        Logging level.
    """
    logging.setLoggerClass(CustomLogger)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(current_dir, 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f"{timestamp}_{class_name}.log"
    log_path = os.path.join(logs_dir, log_filename)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "standard"
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "formatter": "standard",
                "filename": log_path,
                "mode": "a",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": default_level,
        }
    }

    logging.config.dictConfig(logging_config)
