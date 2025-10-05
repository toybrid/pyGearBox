from pyGearBox.plugin import PyGearBoxBasePlugin

class PyGearBoxPlugin(PyGearBoxBasePlugin):
    def __init__(self):
        super().__init__()

    def run(self):
        print("Running: Hello, World!")

    @property
    def name(self):
        return f'simple_hello_world'

    @property
    def version(self):
        return '0.0.1'