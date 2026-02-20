from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from PersonioClient.Data.Meta import Meta
from PersonioClient.Data.ReferenceObject import ReferenceObject


@dataclass
class ProfilePicture:
    url: str


@dataclass
class CustomAttribute:
    id: str
    type: str
    value: str | int
    global_id: str


@dataclass
class Person:
    id: str
    email: str
    created_at: datetime
    updated_at: datetime
    first_name: str
    last_name: str
    preferred_name: Optional[str]
    gender: str
    profile_picture: ProfilePicture
    status: str
    custom_attributes: List[CustomAttribute]
    employments: List[ReferenceObject]
    _meta: Meta
