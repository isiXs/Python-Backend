from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    id : str | None = Field(default = None)
    username: str
    email: str
    