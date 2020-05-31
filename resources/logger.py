"""
open_cdn.server
~~~~~~~~~~~~

This module implements the logger.
:copyright: (c) 2020 by AdriBloober.
:license: GNU General Public License v3.0
"""


from datetime import datetime
from enum import Enum
from os.path import exists
from os import mkdir, listdir, remove

from resources.config import config
from resources.argument_parser import args


class TerminalColors:
    """Define terminal colors to print colored prompt."""

    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


def get_log_directory() -> str:
    """Get the log directory with a '/' at the end."""
    log_dir = config.LOG_DIRECTORY
    if log_dir == "" or log_dir is None:
        log_dir = "logs/"
    if not log_dir.endswith("/"):
        log_dir += "/"

    if not exists(log_dir):
        mkdir(log_dir)

    return log_dir


def parse_log_actions():
    """If the user called any log action in the cli, the log action would be ran here."""
    log_dir = get_log_directory()
    if args.clear_all_logs:
        for file in listdir(log_dir):
            remove(log_dir + file)
        print("All log files has been deleted.")
    elif args.clear_today_log:
        d = datetime.now()
        with open(log_dir + d.strftime(config.LOG_FILENAME), "w") as file:
            file.write("")
        print("The today log has been deleted.")


class LogType(Enum):
    """LogTypes: If the server was not started in verbose mode, INFO logs are not output via stdout."""

    INFO = 0
    WARNING = 1
    ERROR = 2
    CRITICAL = 3
    HIGH = 4

    @staticmethod
    def parse_to_string(log_type, upper=True):
        """Gets the logtype as string.
        :param log_type:
        :param upper: Returns the string in uppercase.
        :return: string
        """
        content = "u"
        if log_type == LogType.INFO:
            content = "i"
        elif log_type == LogType.WARNING:
            content = "w"
        elif log_type == LogType.ERROR:
            content = "e"
        elif log_type == LogType.CRITICAL:
            content = "c"
        elif log_type == LogType.HIGH:
            content = "h"
        if upper:
            content = content.upper()
        return content


class Logger:
    """Logger with log file."""

    def write_log(self, content: str):
        """Write raw log content
        :param content: The content to be written.
        """
        if not content.endswith("\n"):
            content += "\n"
        with open(self.log_file, "a") as file:
            file.write(content)

    def __init__(self):
        parse_log_actions()
        d = datetime.now()
        self.verbose = args.verbose
        self.log_dir = get_log_directory()
        self.log_file = self.log_dir + d.strftime(config.LOG_FILENAME)
        self.write_log("--- Start of log ---")

    def log(self, log_type: LogType, content: str, no_stdout=False):
        """Log something.
        :param log_type: The type of the log message.
        :param content: The content for logging.
        :param no_stdout: Enable it, and the log message would be not logged.
        """
        content = f"{LogType.parse_to_string(log_type)}: {content}\n"
        self.write_log(content)
        if (self.verbose or log_type != LogType.INFO) and not no_stdout:
            if log_type in (LogType.ERROR, LogType.CRITICAL):
                content = TerminalColors.FAIL + content + TerminalColors.ENDC
            elif log_type == LogType.WARNING:
                content = TerminalColors.WARNING + content + TerminalColors.ENDC
            print(content, end="")


logger = Logger()
