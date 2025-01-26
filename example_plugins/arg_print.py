from pyGearBox.plugin import PyGearBoxBasePlugin

class PyGearBoxPlugin(PyGearBoxBasePlugin):
    def __init__(self):
        super().__init__()

    def on_load(self):
        print(self.name + " loaded")

    def on_unload(self):
        print(self.name + " exited")

    def run(self, value):
        print(value)

    @property
    def name(self):
        return 'Argument Printer'

    @property
    def plugin_type(self):
        return 'publisher'