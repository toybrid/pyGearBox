import unittest
from unittest.mock import MagicMock, patch
from typing import Dict, Any
from pyGearBox.manager import PyGearBox, PyGearBoxManifest
from pyGearBox.utils import ErrorSafety, Status, PluginUnLoadError, PluginExecutionError, Runnable

class DummyPlugin:
    def __init__(self, name="dummy", error_safety=ErrorSafety.CONTINUE):
        self.name = name
        self.error_safety = error_safety
        self.loaded = False
        self.unloaded = False
        self.pre_ran = False
        self.ran = False
        self.post_ran = False

    def on_load(self):
        self.loaded = True

    def on_unload(self):
        self.unloaded = True

    def pre_run(self):
        self.pre_ran = True

    def run(self, **kwargs):
        self.ran = True

    def post_run(self):
        self.post_ran = True

    def is_valid(self):
        return True


class TestPyGearBox(unittest.TestCase):
    @patch("pyGearBox.manager.import_module")
    def test_load_plugin_success(self, mock_import_module):
        dummy_plugin = DummyPlugin()
        dummy_plugin_class = MagicMock(return_value=dummy_plugin)
        mock_import_module.return_value.PyGearBoxPlugin = dummy_plugin_class

        manager = PyGearBox()
        manifest = PyGearBoxManifest(name="dummy_plugin")
        runnable = manager.load_plugin(manifest)

        self.assertTrue(dummy_plugin.loaded)
        self.assertIn(runnable, manager.loaded_plugins)

    @patch("pyGearBox.manager.import_module")
    def test_load_plugins_success(self, mock_import_module):
        dummy_plugin = DummyPlugin()
        dummy_plugin_class = MagicMock(return_value=dummy_plugin)
        mock_import_module.return_value.PyGearBoxPlugin = dummy_plugin_class

        manager = PyGearBox()
        manifests = [
            PyGearBoxManifest(name="dummy_plugin1"),
            PyGearBoxManifest(name="dummy_plugin2"),
        ]
        result = manager.load_plugins(manifests)
        self.assertTrue(result)
        self.assertEqual(len(manager.loaded_plugins), 2)
        self.assertIn("dummy_plugin1", manager._load_result)
        self.assertIn("dummy_plugin2", manager._load_result)

    def test_run_plugin_success(self):
        plugin = DummyPlugin()
        plugin.name = "test_plugin"
        plugin.error_safety = ErrorSafety.CONTINUE
        runnable = Runnable(instance=plugin, arguments={})

        manager = PyGearBox()
        status = manager.run_plugin(runnable)

        self.assertTrue(plugin.pre_ran)
        self.assertTrue(plugin.ran)
        self.assertTrue(plugin.post_ran)
        self.assertEqual(status.code, 0)
        self.assertIn("test_plugin", manager.result)

    def test_run_plugin_error_abort(self):
        class FailingPlugin(DummyPlugin):
            def run(self, **kwargs):
                raise Exception("fail!")
        plugin = FailingPlugin(name="fail_plugin", error_safety=ErrorSafety.ABORT)
        runnable = Runnable(instance=plugin, arguments={})

        manager = PyGearBox()
        with self.assertRaises(PluginExecutionError):
            manager.run_plugin(runnable)
        self.assertIn("fail_plugin", manager.result)
        self.assertEqual(manager.result["fail_plugin"].code, 2)

    def test_run_plugin_error_continue(self):
        class FailingPlugin(DummyPlugin):
            def run(self, **kwargs):
                raise Exception("fail!")
        plugin = FailingPlugin(name="fail_plugin", error_safety=ErrorSafety.CONTINUE)
        runnable = Runnable(instance=plugin, arguments={})

        manager = PyGearBox()
        status = manager.run_plugin(runnable)
        self.assertEqual(status.code, 2)
        self.assertIn("fail_plugin", manager.result)

    def test_run_plugins_calls_executor(self):
        manager = PyGearBox()
        dummy_plugin = DummyPlugin(name="plugin1")
        runnable = Runnable(instance=dummy_plugin, arguments={})
        manager._loaded_plugins.append(runnable)

        mock_executor = MagicMock()
        manager.run_plugins(executor=mock_executor)
        mock_executor.execute.assert_called_once_with(manager.loaded_plugins, manager.run_plugin)

    def test_loaded_plugins_property(self):
        manager = PyGearBox()
        dummy_plugin = DummyPlugin(name="plugin1")
        runnable = Runnable(instance=dummy_plugin, arguments={})
        manager._loaded_plugins.append(runnable)
        self.assertEqual(manager.loaded_plugins, [runnable])

    def test_result_property(self):
        manager = PyGearBox()
        manager._result = {"foo": Status(0, "ok", None)}
        self.assertEqual(manager.result, {"foo": Status(0, "ok", None)})

    def test_del_unload_plugins(self):
        manager = PyGearBox()
        dummy_plugin = DummyPlugin(name="plugin1")
        dummy_plugin.error_safety = ErrorSafety.CONTINUE
        runnable = Runnable(instance=dummy_plugin, arguments={})
        manager._loaded_plugins.append(runnable)
        # Call __del__ directly for test
        manager.__del__()
        self.assertTrue(dummy_plugin.unloaded)

    def test_del_unload_plugin_error_abort(self):
        class FailingPlugin(DummyPlugin):
            def on_unload(self):
                raise Exception("fail!")
        plugin = FailingPlugin(name="fail_plugin", error_safety=ErrorSafety.ABORT)
        runnable = Runnable(instance=plugin, arguments={})
        manager = PyGearBox()
        manager._loaded_plugins.append(runnable)
        with self.assertRaises(PluginUnLoadError):
            manager.__del__()


if __name__ == "__main__":
    unittest.main()