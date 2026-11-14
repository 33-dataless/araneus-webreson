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

    '''maybe? if well be gui'''
    async def delete_tool(self):
        pass

    async def change_tool(self):
        pass

