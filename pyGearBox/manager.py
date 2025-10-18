from typing import List, Dict, Optional
from dataclasses import dataclass
from importlib import import_module

from pyGearBox.utils import (
    ErrorSafety,
    Status,
    PluginUnLoadError,
    Runnable,
    PluginExecutionError,
)
from pyGearBox.executors import LinearExecutor


@dataclass
class PyGearBoxMaifest:
    name: str
    arguments: Optional[Dict] = None


class PyGearBox:
    def __init__(self):
        self._loaded_plugins = []
        self._load_result = {}
        self._unload_result = {}
        self._result = {}

    def __del__(self):
        for plugin in self.loaded_plugins:
            try:
                if hasattr(plugin.instance, "on_unload"):
                    plugin.instance.on_unload()
            except Exception as e:
                stat = Status(2, str(e), plugin)
                self._unload_result[plugin.instance.name] = stat
                if plugin.instance.error_safety == ErrorSafety.ABORT:
                    raise PluginUnLoadError(
                        f"Failed to unload plugin: {plugin.instance.name}"
                    )

    def load_plugin(self, plugin_manifest: PyGearBoxMaifest):
        """
        Loads a plugin based on the provided plugin manifest.

        Imports the plugin module, instantiates the plugin class, and validates it using its `is_valid` method.
        If valid, calls the plugin's `on_load` method, wraps it in a Runnable, and adds it to the list of loaded plugins.
        If invalid, records the failure and raises a PluginLoadError.

        Args:
            plugin_manifest (PyGearBoxMaifest): The manifest containing plugin metadata and arguments.

        Returns:
            Runnable: The runnable instance wrapping the loaded plugin.

        Raises:
            PluginLoadError: If the plugin fails validation or cannot be loaded.
        """
        imported_module = import_module(plugin_manifest.name)
        plugin_instance = imported_module.PyGearBoxPlugin()
        if hasattr(plugin_instance, "on_load"):
            plugin_instance.on_load()
        runnable = Runnable(
            instance=plugin_instance, arguments=plugin_manifest.arguments
        )
        self._loaded_plugins.append(runnable)
        return runnable

    def load_plugins(self, manifests: List[PyGearBoxMaifest]):
        """
        Loads plugins based on the provided manifests.
        Iterates through each plugin manifest in `self._manifests`, loads the plugin using
        `load_plugin`, and updates the `_load_result` dictionary with the plugin name and a
        success status. Raises a ValueError if no plugin manifests are provided.
        Raises:
            ValueError: If `self._manifests` is None.
        """

        for plugin_manifest in manifests:
            self.load_plugin(plugin_manifest)
            if plugin_manifest.name not in self._load_result.keys():
                self._load_result[plugin_manifest.name] = Status(
                    0, "SUCCESS", plugin_manifest
                )

    def run_plugin(self, plugin: object) -> Status:
        """
        Executes the specified plugin by calling its pre_run, run, and post_run methods.

        Args:
            plugin (object): The plugin object to execute. It should have an 'instance' attribute
                with 'pre_run', 'run', and 'post_run' methods, as well as 'arguments', 'name',
                and 'error_safety' attributes.

        Returns:
            Status: A Status object indicating the result of the plugin execution.

        Raises:
            PluginExecutionError: If the plugin execution fails and its error_safety is set to ABORT.
        """
        try:
            if hasattr(plugin.instance, "pre_run"):
                plugin.instance.pre_run()

            plugin.instance.run(**plugin.arguments or {})

            if hasattr(plugin.instance, "post_run"):
                plugin.instance.post_run()

            stat = Status(0, "SUCCESS", plugin.instance)
            if plugin.instance.name not in self._result.keys():
                self._result[plugin.instance.name] = stat
                print("its here-----------")
                print(self._result)
        except Exception as e:
            stat = Status(2, f"Error: {e}", plugin)
            if plugin.instance.name not in self._result.keys():
                self._result[plugin.instance.name] = stat
            if plugin.instance.error_safety == ErrorSafety.ABORT:
                raise PluginExecutionError(f"Failed to run plugin '{plugin}': {e}")

        return stat

    def run_plugins(self, executor=LinearExecutor()):
        """
        Executes all loaded plugins using the specified executor.

        Args:
            executor (Executor, optional): The executor instance to use for running plugins.
                Defaults to LinearExecutor().

        Returns:
            None
        """
        executor.execute(self.loaded_plugins, self.run_plugin)

    @property
    def loaded_plugins(self) -> Dict[str, object]:
        """
        Returns a dictionary of currently loaded plugins.

        Returns:
            Dict[str, object]: A dictionary where the keys are plugin names and the values are plugin instances.
        """
        return self._loaded_plugins

    @property
    def result(self) -> Dict[str, Status]:
        """
        Returns the result dictionary containing status information.

        Returns:
            Dict[str, Status]: A dictionary mapping string keys to Status objects.
        """
        return self._result
