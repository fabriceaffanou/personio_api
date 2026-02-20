from typing import Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from PersonioClient.Data.Meta import Meta
from PersonioClient.Data.Person import ProfilePicture, CustomAttribute
from PersonioSyncService.Data.SyncEmployment import SyncEmployment


@dataclass
class SyncPerson:
    id: str
    company_employee_id: str
    email: str
    created_at: datetime
    updated_at: datetime
    first_name: str
    last_name: str
    preferred_name: Optional[str]  # Preferred name can be None
    gender: Optional[str]  #  Gender can be None
    profile_picture: ProfilePicture
    status: str
    custom_attributes: List[CustomAttribute] = field(default_factory=list)
    employments: List[SyncEmployment] = field(default_factory=list)
    meta: Meta = field(default=None)
    sync_action: Optional[str] = field(default=None)

    @classmethod
    def from_obj(cls, obj: Any) -> "SyncPerson":
        return cls(
            id=obj.id,
            company_employee_id=obj.company_employee_id,
            email=obj.email,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            first_name=obj.first_name,
            last_name=obj.last_name,
            preferred_name=obj.preferred_name,
            gender=obj.gender,
            profile_picture=obj.profile_picture,
            status=obj.status,
            custom_attributes=obj.custom_attributes,
            employments=obj.employments or [],
            meta=obj._meta,
            sync_action=obj.sync_action,
        )
