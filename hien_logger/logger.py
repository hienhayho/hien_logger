# This file contains the logger configuration for the application.
import os
import sys
import click
import logging
from copy import copy
from pathlib import Path
from typing import Literal

from .utils import get_date_format

TRACE_LOG_LEVEL = 5


class ColourizedFormatter(logging.Formatter):
    level_colors = {
        TRACE_LOG_LEVEL: "blue",
        logging.DEBUG: "cyan",
        logging.INFO: "green",
        logging.WARNING: "yellow",
        logging.ERROR: "red",
        logging.CRITICAL: "magenta",
    }

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: Literal["%", "{", "$"] = "%",
        use_colors: bool | None = None,
    ):
        """
        Initialize the formatter.

        Args:
            fmt (str | None): The format string. Defaults to `None`.
            datefmt (str | None): The date format string. Defaults to `None`.
            style (Literal["%", "{", "$"]): The style of the format string. Defaults to `%`.
            use_colors (bool | None): Whether to use colors. Defaults to `None`.
        """
        if use_colors in (True, False):
            self.use_colors = use_colors
        else:
            self.use_colors = sys.stdout.isatty()
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def color_level_name(self, level_name: str, level_no: int) -> str:
        """
        Colorize the level name.

        Args:
            level_name (str): The level name.
            level_no (int): The level number.

        Returns:
            str: The colorized level name.
        """
        color = self.level_colors.get(level_no, "reset")
        return click.style(str(level_name), fg=color)

    def color_message(self, message: str, level_no: int) -> str:
        """
        Colorize the message.

        Args:
            message (str): The message.
            level_no (int): The level number.

        Returns:
            str: The colorized message.
        """
        color = self.level_colors.get(level_no, "reset")
        return click.style(str(message), fg=color)

    def color_date(self, record: logging.LogRecord) -> str:
        """
        Apply green color to the date.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            str: The colorized date.
        """
        date_str = self.formatTime(record, self.datefmt)
        return click.style(date_str, fg=(200, 200, 200))

    def should_use_colors(self) -> bool:
        """
        Check if colors should be used. Defaults to `True`.

        Returns:
            bool: Whether colors should be used.
        """
        return self.use_colors

    def formatMessage(self, record: logging.LogRecord) -> str:
        """
        Format the message.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            str: The formatted message.
        """
        recordcopy = copy(record)
        levelname = recordcopy.levelname
        seperator = " " * (8 - len(recordcopy.levelname))

        if self.use_colors:
            relpathname = "/".join(recordcopy.pathname.split("/")[-2:])
            levelname = self.color_level_name(levelname, recordcopy.levelno)
            recordcopy.msg = self.color_message(recordcopy.msg, recordcopy.levelno)
            recordcopy.__dict__["message"] = recordcopy.getMessage()
            recordcopy.asctime = self.color_date(recordcopy)
            recordcopy.__dict__["relpathname"] = relpathname
            recordcopy.__dict__["name"] = self.color_message(
                recordcopy.name, recordcopy.levelno
            )

        recordcopy.__dict__["levelprefix"] = levelname + seperator
        return super().formatMessage(recordcopy)


class DefaultFormatter(ColourizedFormatter):
    def should_use_colors(self) -> bool:
        return sys.stderr.isatty()

    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)

        if "pathname" in recordcopy.__dict__:
            relpathname = "/".join(recordcopy.pathname.split("/")[-2:])
            recordcopy.__dict__["relpathname"] = relpathname
        else:
            recordcopy.__dict__["relpathname"] = (
                "N/A"  # Fallback when pathname is missing
            )

        levelname = recordcopy.levelname
        seperator = " " * (8 - len(levelname))

        if self.use_colors:
            levelname = self.color_level_name(levelname, recordcopy.levelno)
            recordcopy.msg = self.color_message(recordcopy.msg, recordcopy.levelno)
            recordcopy.__dict__["message"] = recordcopy.getMessage()
            recordcopy.asctime = self.color_date(recordcopy)

        recordcopy.__dict__["levelprefix"] = levelname + seperator
        recordcopy.__dict__["pid"] = os.getpid()

        return super().formatMessage(recordcopy)


class FileFormater(logging.Formatter):
    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)

        if "pathname" in recordcopy.__dict__:
            relpathname = "/".join(recordcopy.pathname.split("/")[-2:])
            recordcopy.__dict__["relpathname"] = relpathname
        else:
            recordcopy.__dict__["relpathname"] = (
                "N/A"  # Fallback when pathname is missing
            )

        return super().formatMessage(recordcopy)


def get_formatted_logger(
    name: str, file_path: str | None = None, global_file_log: bool = False
) -> logging.Logger:
    """
    Get a coloured logger.

    Args:
        name (str): The name of the logger.
        file_path (str | None): The path to the log file. Defaults to `None`.
        global_file_log (bool): Whether to log to the global file. Defaults to `False`.

    Returns:
        logging.Logger: The logger object.

    **Note:** Name is only used to prevent from being root logger.
    """
    logger = logging.getLogger(name=name)
    logger.setLevel(TRACE_LOG_LEVEL)
    logger.propagate = False

    if logger.hasHandlers():
        logger.handlers.clear()

    stream_handler = logging.StreamHandler()
    stream_formatter = DefaultFormatter(
        "%(name)s | %(asctime)s - %(pid)s | %(levelprefix)s - [%(relpathname)s %(funcName)s(%(lineno)d)] - %(message)s",
        datefmt="%Y/%m/%d  %H:%M:%S",
    )
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    if file_path:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(file_path)
        file_formatter = FileFormater(
            "%(name)s | %(asctime)s | %(levelname)-8s - [%(relpathname)s %(funcName)s(%(lineno)d)] - %(message)s",
            datefmt="%Y/%m/%d - %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    if global_file_log:
        Path("logs").mkdir(parents=True, exist_ok=True)

        global_file = logging.FileHandler("logs/global.log")
        file_formatter = FileFormater(
            "%(asctime)s | %(levelname)-8s - [%(relpathname)s %(funcName)s(%(lineno)d)] - %(message)s",
            datefmt="%Y/%m/%d - %H:%M:%S",
        )
        global_file.setFormatter(file_formatter)
        logger.addHandler(global_file)

    return logger
