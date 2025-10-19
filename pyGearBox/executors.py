from typing import Callable, List
from typing import Protocol
from pyGearBox.utils import Runnable


class BaseExecutor(Protocol):
    """
    Abstract interface for executors in the pyGearBox framework.
    Executors are responsible for managing the execution of a list of Runnable objects.
    """

    def execute(self, runnables: List[Runnable], runner: Callable):
        pass


class LinearExecutor:
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
