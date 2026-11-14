import logging
from pathlib import Path

from pydantic import ValidationError

from src.json_parser import JsonParser
from .tool_model import ToolModel

log = logging.getLogger(__name__)
class Tools:
    def __init__(self):
        self.path_tools = Path("tools/tools.json")
        self.jparser = JsonParser(path_tools=self.path_tools)
    
    async def add_tool(self, arguments: dict):
        tools = await self.jparser.load_json()

        new_id = str(max(
            (int(tool_id) for tool_id in tools),
            default=0
        ) + 1)

        arguments = {**arguments, "id": new_id}

        try:
            validated_tool = ToolModel.model_validate(arguments)
        except ValidationError as error:
            log.error("Tool validation failed: %s", error)
            raise
        new_config = validated_tool.model_dump(exclude={"id"})

        for tool in tools.values():
            existing_config = {
                key: value
                for key, value in tool.items()
                if key != "id"
            }

            if existing_config == new_config:
                raise ValueError(f"Tool '{validated_tool.name}' with this configuration already exists")

        tools[new_id] = validated_tool.model_dump()
        await self.jparser.dump_json(tools)
        log.info("New instrument id -> %s (%s) recorded successfully",
                 new_id, validated_tool.name)

        return new_id

    async def get_current_tools(self):
        tools = await self.jparser.load_json()

        for i, (tool_id, tool) in enumerate(tools.items()):
            print(f"{i} ~ ID: {tool['id']} | {tool['name']}")


    async def get_current_tools(self):
        tools = await self.jparser.load_json()

        if not tools:
            print("[!] No tools registered")
            return

        for tool_id, tool in tools.items():
            print(
                f"ID: {tool_id} | "
                f"Name: {tool['name']} | "
                f"Executable: {tool['executable']} | "
                f"Args: {' '.join(tool['args'])}"
            )

    async def delete_tool(self, tool_id: str):
        tools = await self.jparser.load_json()

        if tool_id not in tools:
            raise ValueError(f"Tool with ID {tool_id} not found")

        deleted_tool = tools.pop(tool_id)

        await self.jparser.dump_json(tools)

        log.info(
            "Tool deleted: %s (ID: %s)",
            deleted_tool["name"],
            tool_id
        )

    async def change_tool(self, tool_id: str, arguments: dict):
        tools = await self.jparser.load_json()

        if tool_id not in tools:
            raise ValueError(f"Tool with ID {tool_id} not found")

        current_tool = tools[tool_id]

        updated_tool = {
            **current_tool,
            **arguments,
            "id": tool_id
        }

        try:
            validated_tool = ToolModel.model_validate(updated_tool)
        except ValidationError as error:
            log.error("Tool validation failed: %s", error)
            raise

        new_config = validated_tool.model_dump(exclude={"id"})

        for existing_id, tool in tools.items():
            if existing_id == tool_id:
                continue

            existing_config = {
                key: value
                for key, value in tool.items()
                if key != "id"
            }

            if existing_config == new_config:
                raise ValueError(
                    f"Tool '{validated_tool.name}' "
                    "with this configuration already exists"
                )

        tools[tool_id] = validated_tool.model_dump()

        await self.jparser.dump_json(tools)



