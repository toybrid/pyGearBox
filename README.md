# pyGearBox
**PyGearBox** is a powerful, lightweight, and user-friendly plugin manager designed for Python applications. It enables developers to modularize their code by dynamically loading and executing plugins. With PyGearBox, developers can build highly extensible systems that allow easy integration of additional features without modifying the core application logic.

## Key Features
- **Dynamic Plugin Loading:** Load plugins at runtime, reducing code complexity and improving modularity.
- **Easy-to-Use API:** Simple and intuitive methods for loading and executing plugins.
- **Customizable Plugins:** Extend your application by creating custom plugins tailored to your needs.
- **Lightweight and Fast:** Minimal performance overhead, designed with efficiency in mind.
- **Community-Driven:** Fully open source, welcoming contributions and feedback from developers worldwide.
## Example Usage
Below is an example of how to use PyGearBox to manage and execute plugins in your Python application:

```python
from pyGearBox.manager import PyGearBox

# Define a list of plugins to be loaded
plugin_list = [
    'simple_hello_world',  # A plugin that prints a simple message
    'arg_print'            # A plugin that prints a message passed as an argument
]

# Initialize the plugin manager with the list of plugins
gearbox = PyGearBox(plugin_list)

# Load the plugins
gearbox.load_plugins()

# Run the 'simple_hello_world' plugin
gearbox.run_plugin('simple_hello_world')

# Run the 'arg_print' plugin with an argument
gearbox.run_plugin('arg_print', 'Hello, World! from arg')
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