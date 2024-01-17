import importlib


def load_plugins(plugins):
    configured_plugins = {}
    for plugin in plugins:
        module = importlib.import_module(f"station.plugins.{plugin}")
        configured_plugins[plugin] = module

    return configured_plugins


class Core:
    def __init__(self, plugins):
        self.configured_plugins = load_plugins(plugins)

    def display(self):
        for configured_plugin in self.configured_plugins.values():
            configured_plugin.greeting()
