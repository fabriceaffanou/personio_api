from datetime import datetime
from enum import Enum


def to_dict(obj: object) -> dict:
    """Recursively converts an object to a dictionary."""
    if hasattr(obj, "__dict__"):
        result = {}
        for k, v in obj.__dict__.items():
            if isinstance(v, Enum):
                result[k] = v.value
            elif isinstance(v, datetime):
                result[k] = v.isoformat()
            elif isinstance(v, list):
                result[k] = [to_dict(x) for x in v]
            elif hasattr(v, "__dict__"):
                result[k] = to_dict(v)
            else:
                result[k] = v
        return result
    if isinstance(obj, list):
        return [to_dict(x) for x in obj]
    return obj
