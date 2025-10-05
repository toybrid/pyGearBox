import logging as log
from abc import ABC, abstractmethod

from pyGearBox.utils import ErrorSafety
    
class PyGearBoxBasePlugin(ABC):
    """
    Abstract base class for pyGearBox plugins.
    This class defines the interface and lifecycle hooks for plugins in the pyGearBox framework.
    Plugins should inherit from this class and implement the required abstract methods and properties.
    Methods:
        is_valid(): Checks if the plugin class is a valid subclass of PyGearBoxBasePlugin.
        on_load(): Called when the plugin is loaded; logs the plugin name.
        on_unload(): Called when the plugin is unloaded; logs the plugin name.
        pre_run(): Hook called before the plugin's main run method.
        post_run(): Hook called after the plugin's main run method.
        run(): Abstract method; must be implemented to define the plugin's main logic.
    Properties:
        name (str): Abstract property; must be implemented to return the plugin's name.
        plugin_type (str): Abstract property; must be implemented to return the plugin's type.
        version (str): Abstract property; must be implemented to return the plugin's version.
        error_safety: Returns the error safety mode for the plugin (default: ErrorSafety.CONTINUE).
    Special Methods:
        __str__(): Returns a string representation of the plugin as 'name/plugin_type'.
        __repr__(): Returns a detailed string representation including version as 'name/plugin_type/vversion'.
    """

    def is_valid(self):
        return issubclass(self.__class__, PyGearBoxBasePlugin)

    def on_load(self):
        print(f'Plugin {self.name} loaded')

    def on_unload(self):
        print(f'Plugin {self.name} unloaded')

    def pre_run(self):
        pass

    def post_run(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def version(self):
        pass

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}/{self.version}'
    
    @property
    def error_safety(self):
        return ErrorSafety.ABORT