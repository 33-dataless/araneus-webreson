from pydantic import BaseModel, Field, ConfigDict

class ToolModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    executable: str = Field(min_length=1)
    args: list[str]
