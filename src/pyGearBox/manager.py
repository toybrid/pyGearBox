import sys
from importlib import import_module
from pathlib import Path


class PyGearBox:
    """
    PyGearBox is a manager class for handling plugins.
    Attributes:
        _plugin_list (list): A list of plugin names to be loaded.
        _loaded_plugins (dict): A dictionary of loaded plugin instances.
    Methods:
        __init__(plugin_list: list):
            Initializes the PyGearBox with a list of plugins.
        __del__():
            Unloads all loaded plugins upon deletion of the PyGearBox instance.
        get_plugin(plugin: str):
            Retrieves a loaded plugin instance by its name.
        load_plugins():
            Loads and initializes all plugins from the plugin list.
        run_plugin(plugin_name: str, *args, **kwargs):
            Runs a specified plugin with given arguments.
        loaded_plugins:
            Returns the dictionary of loaded plugins.
        plugin_list:
            Returns the list of plugin names.
    """
    def __init__(self, plugin_list: list):
        """
        Initializes the Manager with a list of plugins.

        Args:
            plugin_list (list): A list of plugins to be managed.
        """
        self._plugin_list = plugin_list
        self._loaded_plugins = {}

    def __del__(self):
        """
        Destructor method that is called when the instance is about to be destroyed.
        
        This method iterates over all loaded plugins and calls their `on_unload` method
        to perform any necessary cleanup before the instance is destroyed.
        """
        for plugin in self._loaded_plugins.values():
            plugin.on_unload()

    def get_plugin(self, plugin: str):
        """
        Retrieve a loaded plugin by its name.

        Args:
            plugin (str): The name of the plugin to retrieve.

        Returns:
            The plugin object if found, otherwise None.
        """
        return self._loaded_plugins.get(plugin, None)

    def load_plugins(self):
        """
        Loads and initializes plugins from the plugin list.

        This method iterates through the list of plugins specified in `self.plugin_list`,
        attempts to import each plugin module, and creates an instance of the plugin class.
        If the plugin instance is valid, it calls the `on_load` method of the plugin and
        stores the instance in the `_loaded_plugins` dictionary.

        Raises:
            ImportError: If a plugin module cannot be imported.

        Prints:
            An error message to `sys.stderr` if a plugin fails to import.

        """
        for plugin in self.plugin_list:
            try:
                imported_module = import_module(plugin)
                plugin_instance = imported_module.PyGearBoxPlugin()
                if plugin_instance.is_valid():
                    plugin_instance.on_load()
                    self._loaded_plugins[plugin] = plugin_instance
            except ImportError as e:
                print(f"Failed to import plugin '{plugin}': {e}", file=sys.stderr)

    def run_plugin(self, plugin_name:str, *args, **kwargs):
        """
        Executes the specified plugin with the given arguments.

        This method retrieves the plugin by its name, and if found, it executes
        the plugin's `pre_run`, `run`, and `post_run` methods in sequence.

        Args:
            plugin_name (str): The name of the plugin to run.
            *args: Variable length argument list to pass to the plugin's `run` method.
            **kwargs: Arbitrary keyword arguments to pass to the plugin's `run` method.

        Raises:
            ValueError: If the specified plugin is not found.
        """
        plugin = self.get_plugin(plugin_name)
        if plugin is None:
            raise ValueError(f"Plugin '{plugin_name}' not found")
        plugin.pre_run()
        plugin.run(*args, **kwargs)
        plugin.post_run()

    @property
    def loaded_plugins(self):
        """
        Property that returns the list of loaded plugins.

        Returns:
            list: A list of loaded plugins.
        """
        return self._loaded_plugins
    
    @property
    def plugin_list(self):
        """
        Retrieve the list of plugins.

        Returns:
            list: A list containing the plugins.
        """
        return self._plugin_list
