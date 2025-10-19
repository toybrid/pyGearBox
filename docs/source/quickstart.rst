Quickstart
========================

Write a simple plugin
------------------------

To write a simple plugin developer need to implement minimum two methods to a class, The class name should be same as in the
example, save this file as `simple_hello_world.py`

.. code-block:: python

    from pyGearBox.utils import ErrorSafety

    class PyGearBoxPlugin:
        def run(self):
            print("Hello, World!")

        def error_safety(self):
            return ErrorSafety.CONTINUE

Run the plugin via Plugin Manager
---------------------------------
Once you make a plugin you can run it via plugin manager as shown below:, you could provide any list of plugins to the 
PluginManager, when you create a plugin manifest you provide the module name, `simple_hello_world` is the name of the module
itself without the `.py` extension

.. code-block:: python

    from pyGearBox.manager import PyGearBox, PyGearBoxManifest

    plugin_list = [
            PyGearBoxManifest(name="simple_hello_world"),
        ]

    gearbox = PyGearBox()
    gearbox.load_plugins(plugin_list)
    gearbox.run_plugins()

Run the single plugin via Plugin Manager
----------------------------------------
Instead of running all the plugins at once, you can run a single plugin by specifying it in the
`run_plugin` method of the `PyGearBox` instance. Here's how you can do it:

.. code-block:: python

    from pyGearBox.manager import PyGearBox, PyGearBoxManifest

    plugin_manifest = PyGearBoxManifest(name='simple_hello_world')

    gearbox = PyGearBox()
    plugin = gearbox.load_plugin(plugin_manifest)
    gearbox.run_plugin(plugin)

Advanced plugin
-----------------
You can also create advanced plugins by implementing additional lifecycle methods such as `on_load`, `on_unload`, `pre_run`, and `post_run`.
Here's an example of an advanced plugin:

.. code-block:: python

    from pyGearBox.utils import ErrorSafety

    class PyGearBoxPlugin:
        def on_load(self):
            print("Advanced Plugin Loaded")

        def on_unload(self):
            print("Advanced Plugin Unloaded")

        def run(self):
            print("Hello from Advanced Plugin!")

        def pre_run(self):
            print("Preparing to run Advanced Plugin")

        def post_run(self):
            print("Finished running Advanced Plugin")

        def error_safety(self):
            return ErrorSafety.CONTINUE

Error management
-----------------
Plugins can define their error management strategy by implementing the `error_safety` property. 
The available strategies are defined in the `ErrorSafety` enum:

- **ABORT**: Stop execution on error
- **CONTINUE**: Continue execution despite errors

Here's an example of a plugin that uses the `ABORT` strategy:

.. code-block:: python

    from pyGearBox.utils import ErrorSafety

    class PyGearBoxPlugin:
        def run(self):
            print("This plugin will abort on error")

        @property
        def error_safety(self):
            return ErrorSafety.ABORT

You can then load and run this plugin using the `PyGearBox` manager as shown earlier. This plugin will fail further 
execution if an error occurs during its execution.

If you have all plugins with ErrorSafety.CONTINUE, even if one plugin fails the rest of the plugins will continue to execute.
You can parse all results of each plugin later with result property of the PyGearBox instance.

.. code-block:: python

    from pyGearBox.manager import PyGearBox, PyGearBoxManifest

    plugin_list = [
            PyGearBoxManifest(name="simple_hello_world"),
            PyGearBoxManifest(name="advanced_plugin"),
            PyGearBoxManifest(name="abort_on_error_plugin"),
        ]

    gearbox = PyGearBox()
    gearbox.load_plugins(plugin_list)
    gearbox.run_plugins()

    for result in gearbox.results:
        print(gearbox.results[result].code, gearbox.results[result].message)