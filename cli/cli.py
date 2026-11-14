import os

from cli_parser import Parser
from tools.tools import Tools

class Cli:
    def __init__(self):
        self.args = Parser().parse()
        self.tools = Tools()

    def flag_add_tool(self):
        if len(self.args.add_tool) < 2:
            raise ValueError(
                "Usage: --add-tool NAME EXECUTABLE [ARGS...]"
            )

        name = self.args.add_tool[0]
        executable = self.args.add_tool[1]
        arguments = self.args.add_tool[2:]

        tools.add_tool(
            {
                "name": name,
                "executable": executable,
                "args": arguments
            }
        )

    def flag_domain(self):
        pass






