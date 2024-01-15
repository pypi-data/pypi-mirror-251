from nwon_baseline.typings import AnyDict as AnyDict
from pydantic import BaseModel as BaseModel

def pydantic_model_to_dict(model: BaseModel) -> AnyDict: ...
