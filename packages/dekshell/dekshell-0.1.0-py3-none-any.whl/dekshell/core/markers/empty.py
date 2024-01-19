from .base import MarkerBase
from ...utils.shell import shell_command


class EmptyMarker(MarkerBase):
    tag_head = ""

    def exec(self, env, command, marker_node, marker_set):
        command = self.strip(command)
        if command:
            kwargs = marker_node.payload or {}
            env.shell(command, ShellCommand(kwargs))


class ShellCommand:
    def __init__(self, kwargs):
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        kwargs = kwargs | self.kwargs
        return shell_command(*args, **kwargs)
