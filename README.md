# pyGearBox
**PyGearBox** is a powerful, lightweight, and user-friendly plugin manager designed for Python applications. It enables developers to modularize their code by dynamically loading and executing plugins. With PyGearBox, developers can build highly extensible systems that allow easy integration of additional features without modifying the core application logic.

## Key Features
- **Dynamic Plugin Loading:** Load plugins at runtime, reducing code complexity and improving modularity.
- **Easy-to-Use API:** Simple and intuitive methods for loading and executing plugins.
- **Customizable Plugins:** Extend your application by creating custom plugins tailored to your needs.
- **Lightweight and Fast:** Minimal performance overhead, designed with efficiency in mind.
- **Community-Driven:** Fully open source, welcoming contributions and feedback from developers worldwide.
- **Task Executor** Ability to scale different types of processing like threaded, parallel, async etc
## Example Usage
Below is an example of how to use PyGearBox to manage and execute plugins in your Python application:

```python
from pyGearBox.manager import PyGearBox, PyGearBoxManifest

# Initialize the plugin manager
gearbox = PyGearBox()

# Run the 'simple_hello_world' plugin
simple_plugin = PyGearBoxManifest(name='simple_hello_world')
plugin = gearbox.load_plugin(simple_plugin)
gearbox.run_plugin(plugin)

# Results
>> simple_hello_world loaded
>> Running: Hello, World!

# # Run the 'arg_print' plugin with an argument
arg_plugin = PyGearBoxManifest(name='arg_print', arguments={'custom': 'Hello', 'value': 'World! from arg'})
plugin = gearbox.load_plugin(arg_plugin)
gearbox.run_plugin(plugin)

# Results
>> arg_print loaded
>> Running arg_print plugin
>> Hello World! from arg

gearbox.run_plugins()

for i in gearbox.result:
    print(gearbox.result[i])

>> Status(code=0, message="Successfully ran plugin 'Runnable(instance=<simple_hello_world.PyGearBoxPlugin object at 0x1049c4510>, arguments=None)'")
>> Status(code=0, message="Successfully ran plugin 'Runnable(instance=<arg_print.PyGearBoxPlugin object at 0x104cce210>, arguments={'custom': 'Hello', 'value': 'World! from arg'})'")
```
# Run All Plugins
```python

plugin_list = [
        PyGearBoxMaifest(name="simple_hello_world"),
        PyGearBoxMaifest(
            name="arg_print", arguments={"custom": "Hello", "value": "World! from arg"}
        ),
    ]

gearbox = PyGearBox()
gearbox.load_plugins(plugin_list)
gearbox.run_plugins()
```
## Plugin Discovery in PyGearBox
PyGearBox is designed to provide a seamless plugin discovery mechanism, making it easy for developers to load plugins dynamically. Here's how the plugin discovery process works:

### Example Scenarios
`plugins` directory in below examples are available in PYTHONPATH

Direct File Plugins:
A plugin named `simple_hello_world` located as a standalone file in the plugin path:
```python
plugins/
└── simple_hello_world.py
```
Package and Module Plugins:
A plugin named `advanced.greetings` is part of a package:
```python
plugins/
└── advanced/
    ├── __init__.py
    └── greetings.py
```
In this case, the plugin is referenced as advanced.greetings during initialization.

## Example Plugins

**Minimal Plugin**

```python
from pyGearBox.plugin import PyGearBoxBasePlugin

class PyGearBoxPlugin(PyGearBoxBasePlugin):
    def __init__(self):
        super().__init__()

    def run(self):
        print("Hello, World!")

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def version(self):
        return '1.0.2'
```

## Task Executor

**Linear Executor**
- Simple task / process executor, runs one after the other in a for loop

## Plugin Features
You can implement the below methods on the plugin to implement code execution at different stages of plugin management

- **on_load:** Executed when the plugin is loaded, used for initialization tasks.
- **on_unload:** Executed when the plugin is unloaded, used for cleanup tasks.
- **pre_run:** Executed before the main run function, used for setup or pre-processing.
- **post_run:** Executed after the main run function, used for teardown or post-processing.
- **run:** The main function of the plugin, where its core functionality is implemented.

## Upcoming Features

**Parallel Executor (WIP / Future)**
- execute task / process executor, in parallel prcosses 
- Use python `ProcessPoolExecutor`

**Async Executor (WIP / Future)**
- execute task / process executor, in asyncronised manner
- Use python native async

**Custom directory plugin discovery**
- Currently plugin discovery is based on PYTHONATH will introduce custom directory based plugin discovery