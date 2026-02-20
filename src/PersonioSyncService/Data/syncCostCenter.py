from dataclasses import dataclass


@dataclass
class SyncCostCenter:
    id: str
    name: str
    weight: float

    @classmethod
    def from_obj(cls, obj: dict) -> "SyncCostCenter":
        return cls(
            id=obj.get("id"),
            name=obj.get("name"),
            weight=obj.get("weight", 0.0),
        )
