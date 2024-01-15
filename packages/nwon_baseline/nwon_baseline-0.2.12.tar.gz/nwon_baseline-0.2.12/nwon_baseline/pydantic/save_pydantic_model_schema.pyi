from pydantic import BaseModel as BaseModel
from typing import Type

def save_pydantic_model_schema(pydantic_model: Type[BaseModel], file_path: str) -> str: ...
