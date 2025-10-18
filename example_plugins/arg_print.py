from pyGearBox.utils import ErrorSafety


class PyGearBoxPlugin:
    def __init__(self):
        super().__init__()

    def on_load(self):
        print("arg_print plugin loaded")

    def on_unload(self):
        print("arg_print plugin exited")

    def pre_run(self):
        raise IOError("Simulated pre_run error in arg_print plugin")

    def run(self, custom, value):
        # time.sleep(3)
        print("Running arg_print plugin")
        # print(custom, value)

    def post_run(self):
        print("Finished running arg_print plugin")

    @property
    def name(self):
        return "arg_print"

    @property
    def version(self):
        return "0.1.0"

    def error_safety(self):
        return ErrorSafety.ABORT
