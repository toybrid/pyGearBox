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
class PyGearBoxManifest:
    """
    Represents the manifest for a PyGearBox component.

    Attributes:
        name (str): The name of the plugin.
        arguments (Optional[Dict]): Optional dictionary of arguments associated with the plugin.
    """
    name: str
    arguments: Optional[Dict] = None


class PyGearBox:
    def __init__(self):
        self._loaded_plugins = []
        self._load_result = {}
        self._unload_result = {}
        self._result = {}

    def __del__(self):
        """
        Destructor method that attempts to unload all loaded plugins by calling their `on_unload` method if available.
        If an exception occurs during the unloading of a plugin, it records the error status and, depending on the plugin's
        error safety policy, may raise a `PluginUnLoadError` to abort the process.

        Exceptions:
            PluginUnLoadError: Raised if a plugin fails to unload and its error safety policy is set to ABORT.
        """
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

    def load_plugin(self, plugin_manifest: PyGearBoxManifest):
        """
        Loads a plugin based on the provided plugin manifest.

        Imports the plugin module, instantiates the plugin class, and validates it using its `is_valid` method.
        If valid, calls the plugin's `on_load` method, wraps it in a Runnable, and adds it to the list of loaded plugins.
        If invalid, records the failure and raises a PluginLoadError.

        Args:
            plugin_manifest (PyGearBoxManifest): The manifest containing plugin metadata and arguments.

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

    def load_plugins(self, manifests: List[PyGearBoxManifest])-> bool:
        """
        Loads a list of plugins based on their manifests.

        Iterates through the provided list of PyGearBoxManifest objects, loading each plugin
        using the `load_plugin` method. After attempting to load each plugin, it checks if the
        plugin's name is present in the `_load_result` dictionary. If not, it adds an entry
        indicating a successful load.

        Args:
            manifests (List[PyGearBoxManifest]): A list of plugin manifest objects to load.

        Returns:
            bool: True if all plugins are processed.
        """

        for plugin_manifest in manifests:
            self.load_plugin(plugin_manifest)
            if plugin_manifest.name not in self._load_result.keys():
                self._load_result[plugin_manifest.name] = Status(
                    0, "SUCCESS", plugin_manifest
                )
        return True

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
