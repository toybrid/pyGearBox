import time
from pyGearBox.plugin import PyGearBoxBasePlugin

class PyGearBoxPlugin(PyGearBoxBasePlugin):
    def __init__(self):
        super().__init__()

    def run(self, custom, value):
        # time.sleep(3)
        print("Running arg_print plugin")
        print(custom, value)

    @property
    def name(self):
        return f'arg_print'

    @property
    def version(self):
        return '0.1.0'