import logging as log

from abc import ABC, abstractmethod

class PyGearBoxBasePlugin(ABC):

    def is_valid(self):
        """
        Check if the current class is a subclass of PyGearBoxBasePlugin.

        Returns:
            bool: True if the current class is a subclass of PyGearBoxBasePlugin, False otherwise.
        """
        if issubclass(self.__class__, PyGearBoxBasePlugin):
            return True
        else:
            return False

    def on_load(self):
        log.debug(self.name + " loaded")

    def on_unload(self):
        log.debug(self.name + " exited")

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
    def plugin_type(self):
        pass