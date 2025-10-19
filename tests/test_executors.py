import unittest
from unittest.mock import Mock, call
from pyGearBox.executors import LinearExecutor

class DummyRunnable:
    def __init__(self, name):
        self.name = name

class TestLinearExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = LinearExecutor()

    def test_execute_calls_runner_for_each_runnable(self):
        runnables = [DummyRunnable("a"), DummyRunnable("b"), DummyRunnable("c")]
        runner = Mock()

        self.executor.execute(runnables, runner)

        self.assertEqual(runner.call_count, 3)
        runner.assert_has_calls([call(runnables[0]), call(runnables[1]), call(runnables[2])])

    def test_execute_with_empty_runnables(self):
        runnables = []
        runner = Mock()

        self.executor.execute(runnables, runner)

        runner.assert_not_called()

    def test_execute_runner_side_effect(self):
        runnables = [DummyRunnable("x")]
        called = []

        def runner(runnable):
            called.append(runnable.name)

        self.executor.execute(runnables, runner)
        self.assertEqual(called, ["x"])

if __name__ == "__main__":
    unittest.main()