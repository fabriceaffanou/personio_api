from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from PersonioClient.Data.Meta import Meta


class OrgUnitType(str, Enum):
    team = "team"
    department = "department"


@dataclass
class OrgUnit:
    id: str
    name: str
    type: OrgUnitType
    abbreviation: Optional[str]
    description: Optional[str]
    resource_uri: Optional[str]
    create_time: datetime
    _meta: Meta
