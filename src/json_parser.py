import json
from pathlib import Path

class JsonParser:
    def __init__(self, path_tools: Path):
        self.path_tools = path_tools

        if not path_tools.exists():
            raise FileExistsError(f"script cant find {path_tools}")
            
    async def load_json(self) -> dict:
        with open(self.path_tools, "r", encoding="utf-8") as file:
            tools = json.load(file)
        return tools

    async def dump_json(self, tools: dict):
        '''custom write to json'''
        with self.path_tools.open("w", encoding="utf-8") as file:
            file.write("{\n")

            items = list(tools.items())

            for index, (name, args) in enumerate(items):
                json_name = json.dumps(name, ensure_ascii=False)
                json_args = json.dumps(args, ensure_ascii=False)

                comma = "," if index < len(items) -1 else ""
                 
                file.write(f"    {json_name}: {json_args}{comma}\n")
            
            file.write("}")