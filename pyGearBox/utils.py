from typing import Optional, Dict
from enum import Enum
from dataclasses import dataclass

@dataclass
class Runnable:
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

    def __str__(self):
        return f'Status(code={self.code}, message="{self.message}")'
    
class ErrorSafety(Enum):
    """
    Enum class to represent error safety levels.
    Attributes:
        SAFE: Indicates that the operation is safe and can proceed without issues.
        UNSAFE: Indicates that the operation is unsafe and may lead to issues.
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
        return f'PluginLoadError: {self.message}'
    
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
        return f'PluginLoadError: {self.message}'
    

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
        return f'PluginLoadError: {self.message}'