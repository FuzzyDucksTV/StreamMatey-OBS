"""
The `logger.py` script is a custom logging module for the StreamMatey OBS Plugin software. It provides a `Logger` class for creating logger instances with both console and file handlers, and includes several methods for logging messages, exceptions, and function execution times.

The `Logger` class begins by defining a dictionary of log levels for reference. In the constructor, it takes several parameters:

- `name`: The name of the logger.
- `log_file`: The path to the log file.
- `max_log_file_size`: The maximum size of the log file before it is rotated.
- `max_backup_log_files`: The maximum number of backup log files to keep.
- `console_log_level`: The log level for the console handler (default is WARNING).
- `file_log_level`: The log level for the file handler (default is DEBUG).

The constructor sets up the logger with a console handler and a file handler. The console handler logs messages to the console, while the file handler logs messages to a file and rotates the file when it reaches the maximum size. The handlers are set to different log levels and are formatted differently.

The `Logger` class includes several methods for logging:

- `log_message(level, message)`: Logs a message at the specified level. If the level is invalid, it logs an error message.
- `log_exception(exc)`: Logs an exception as an error message and its traceback as a debug message.
- `log_function_execution_time(func)`: A decorator for logging the execution time of a function. It wraps the function and logs the time it takes to execute as a debug message.

The script also creates a `Logger` instance named 'StreamMatey' that logs to 'app.log', with a maximum file size of 2000 bytes and a maximum of 5 backup files. The console handler is set to the WARNING level and the file handler is set to the DEBUG level.

Finally, the script includes some usage examples of the `Logger` class, demonstrating how to use the `log_function_execution_time` decorator, how to log an exception, and how to log a message.
"""

import logging
from logging.handlers import RotatingFileHandler
import time
import traceback
import functools

class Logger:
    LOG_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    def __init__(self, name, log_file, max_log_file_size, max_backup_log_files, console_log_level=logging.WARNING, file_log_level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_log_level)
        console_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))

        file_handler = RotatingFileHandler(log_file, maxBytes=max_log_file_size, backupCount=max_backup_log_files)
        file_handler.setLevel(file_log_level)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def log_message(self, level, message):
        if level not in self.LOG_LEVELS:
            self.logger.error(f"Invalid log level: {level}")
            return
        log_method = getattr(self.logger, level.lower())
        log_method(message)

    def log_exception(self, exc):
        self.logger.error(f"Exception occurred: {str(exc)}")
        self.logger.debug(traceback.format_exc())

    def log_function_execution_time(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            self.logger.debug(f"{func.__name__} executed in {execution_time} seconds")
            return result
        return wrapper

logger = Logger('StreamMatey', 'app.log', 2000, 5, logging.WARNING, logging.DEBUG)

# Usage examples
@logger.log_function_execution_time
def some_function():
    # Some code here
    pass

try:
    # Some code here
    pass
except Exception as e:
    logger.log_exception(e)

logger.log_message('INFO', 'This is an info message')
