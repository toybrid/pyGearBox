from typing import Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass


@dataclass
class Runnable:
    """
    A class representing a runnable entity with associated instance and arguments.

    Attributes:
        instance (object): The instance to be run.
        arguments (Optional[Dict]): Optional dictionary of arguments for the runnable instance.
    """

    instance: object
    arguments: Optional[Dict] = None


@dataclass
class Status:
    """
    Represents the status of an operation.
    Attributes:
        code (int): Status code (0: success, 1: warning, 2: error).
        message (str): Status message.
    """

    code: int = 0
    message: str = "SUCCESS"
    entity: Any = None


class ErrorSafety(Enum):
    """
    An enumeration that defines error handling strategies.

    Attributes:
        CONTINUE (int): Indicates that execution should continue after an error.
        ABORT (int): Indicates that execution should abort upon encountering an error.
    """

    CONTINUE = 0
    ABORT = 1


class PluginLoadError(Exception):
    """
    Custom exception for plugin loading errors.
    Attributes:
        message (str): Error message.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"PluginLoadError: {self.message}"


class PluginUnLoadError(Exception):
    """
    Custom exception for plugin loading errors.
    Attributes:
        message (str): Error message.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"PluginLoadError: {self.message}"


class PluginExecutionError(Exception):
    """
    Custom exception for plugin loading errors.
    Attributes:
        message (str): Error message.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"PluginLoadError: {self.message}"
