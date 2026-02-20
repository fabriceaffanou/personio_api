from dataclasses import dataclass
from typing import Any


@dataclass
class ReferenceObject:
    id: str

    @staticmethod
    def from_dict(obj: Any) -> "ReferenceObject":
        return ReferenceObject(id=obj.get("id"))
