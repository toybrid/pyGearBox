class PyGearBoxPlugin:
    def __init__(self):
        super().__init__()

    def on_load(self):
        print("simple_hello_world plugin loaded")

    def on_unload(self):
        print("simple_hello_world plugin exited")

    def pre_run(self):
        print("Preparing to run simple_hello_world plugin")

    def run(self):
        print("Running: Hello, World!")

    def post_run(self):
        print("Finished running simple_hello_world plugin")

    @property
    def name(self):
        return "simple_hello_world"

    @property
    def version(self):
        return "0.0.1"
