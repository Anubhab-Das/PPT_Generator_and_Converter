# tool_registry.py
class ToolRegistry:
    _registry = {}

    @classmethod
    def register(cls, name, tool):
        cls._registry[name] = tool

    @classmethod
    def get_tool(cls, name):
        return cls._registry.get(name)

    @classmethod
    def list_tools(cls):
        return list(cls._registry.keys())
