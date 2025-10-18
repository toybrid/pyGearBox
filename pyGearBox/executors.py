from typing import Callable, List
from abc import ABC, abstractmethod
from pyGearBox.utils import Runnable


class BaseExecutor(ABC):
    """
    Abstract base class for plugin executors.
    """

    @abstractmethod
    def execute(self, runnables: List[Runnable], runner: Callable):
        pass


class LinearExecutor(BaseExecutor):
    def __init__(self):
        super().__init__()

    def execute(self, runnables: List[Runnable], runner: Callable):
        """
        Executes a list of Runnable objects using the provided runner function.

        Args:
            runnables (List[Runnable]): A list of Runnable instances to be executed.
            runner (Callable): A function that takes a Runnable as an argument and executes it.

        Returns:
            None
        """
        for runnable in runnables:
            runner(runnable)
