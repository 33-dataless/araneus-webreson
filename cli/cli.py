
import logging
import shlex

from .cli_parser import Parser
from tools.tools import Tools
from service.manager import Manager

log = logging.getLogger(__name__)


class Cli:
    def __init__(self):
        self.args = Parser().parse()
        self.tools = Tools()

    async def add_tool(self):
        arguments = self.args.add_tool

        if len(arguments) < 2:
            raise ValueError(
                "Usage: --add-tool NAME EXECUTABLE [ARGS...]"
            )

        name = arguments[0]
        executable = arguments[1]
        args = arguments[2:]

        required = []

        if any("{domain}" in arg for arg in args):
            required.append("domain")

        tool_config = {
            "name": name,
            "executable": executable,
            "args": args,
            "required": required
        }

        tool_id = await self.tools.add_tool(tool_config)

        print(f"[+] Tool added with ID: {tool_id}")

    async def list_tools(self):
        await self.tools.get_current_tools()

    async def delete_tool(self):
        tool_id = self.args.delete_tool

        await self.tools.delete_tool(tool_id)

        print(f"[+] Tool {tool_id} deleted")

    async def edit_tool(self):
        tool_id = self.args.edit_tool

        current_tools = await self.tools.jparser.load_json()

        if tool_id not in current_tools:
            raise ValueError(f"Tool with ID {tool_id} not found")

        current = current_tools[tool_id]

        print(f"\nEditing tool: {current['name']}")
        print("Press Enter to keep the current value.\n")

        name = input(f"Name [{current['name']}]: ").strip()
        executable = input(
            f"Executable [{current['executable']}]: "
        ).strip()

        current_args = " ".join(current["args"])

        args = input(f"Arguments [{current_args}]: ").strip()

        updated_config = {
            "name": name or current["name"],
            "executable": executable or current["executable"],
            "args": shlex.split(args) if args else current["args"],
        }

        updated_config["required"] = (
            ["domain"]
            if any("{domain}" in arg for arg in updated_config["args"])
            else []
        )

        await self.tools.change_tool(tool_id, updated_config)

        print(f"[+] Tool {tool_id} updated successfully")

    async def scan(self):
        manager = Manager(domain=self.args.domain)
        await manager.runtime()

    async def run(self):
        if self.args.add_tool is not None:
            await self.add_tool()

        elif self.args.list_tools:
            await self.list_tools()

        elif self.args.delete_tool is not None:
            await self.delete_tool()

        elif self.args.edit_tool is not None:
            await self.edit_tool()

        elif self.args.domain:
            await self.scan()
