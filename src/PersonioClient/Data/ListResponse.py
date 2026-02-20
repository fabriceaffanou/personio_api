from typing import Any, Generic, List, Type, TypeVar

import marshmallow
import marshmallow_dataclass
from PersonioClient.Data.Meta import Meta

T = TypeVar("T")


class ListResponse(Generic[T]):
    data: List[T]
    meta: Meta

    def __init__(self, t_class: Type[T], obj: Any):
        self.data = [
            marshmallow_dataclass.class_schema(t_class)(
                unknown=marshmallow.EXCLUDE
            ).load(y)
            for y in obj.get("_data")
        ]
        self.meta = marshmallow_dataclass.class_schema(Meta)().load(obj.get("_meta"))
