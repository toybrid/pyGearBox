from typing import Protocol

from pyGearBox.utils import ErrorSafety


class PyGearBoxPluginInterface(Protocol):
    """
    Abstract base class for pyGearBox plugins.
    This class defines the interface and lifecycle hooks for plugins in the pyGearBox framework.
    Plugins should inherit from this class and implement the required abstract methods and properties.
    Methods:
        on_load(): Called when the plugin is loaded; logs the plugin name.
        on_unload(): Called when the plugin is unloaded; logs the plugin name.
        pre_run(): Hook called before the plugin's main run method.
        post_run(): Hook called after the plugin's main run method.
        run(): Abstract method; must be implemented to define the plugin's main logic.
    Properties:
        error_safety: Returns the error safety mode for the plugin (default: ErrorSafety.CONTINUE).
    """

    def on_load(self):
        pass

    def on_unload(self):
        pass

    def pre_run(self):
        pass

    def post_run(self):
        pass

    def run(self):
        pass

    @property
    def error_safety(self):
        return ErrorSafety.CONTINUE
