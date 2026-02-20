from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, TypeVar, Type
from PersonioClient.Data import Employment
from PersonioClient.Data.Meta import Meta
from PersonioClient.Data.ReferenceObject import ReferenceObject
from PersonioClient.Data.LegalEntity import LegalEntity
from PersonioClient.Data.OrgUnit import OrgUnit
from PersonioClient.Data.Person import Person
from PersonioClient.Data.Employment import EmploymentType
from PersonioClient.Data.Employment import EmploymentStatus
from PersonioClient.Data.Employment import Termination
from PersonioClient.Data.Employment import Position
from PersonioSyncService.Data.syncCostCenter import SyncCostCenter

T = TypeVar("T", bound="SyncEmployment")


@dataclass
class SyncEmployment:
    id: str
    status: EmploymentStatus
    weekly_working_hours: float
    full_time_weekly_working_hours: float
    probation_end_date: Optional[datetime]
    employment_end_date: Optional[datetime]
    employment_start_date: datetime
    type: EmploymentType
    contract_end_date: Optional[datetime]
    cost_centers: List[SyncCostCenter]
    created_at: datetime
    legal_entity: Optional[LegalEntity]
    office: Optional[str]
    org_units: Optional[List[OrgUnit]]
    person: Person
    position: Optional[Position]
    sub_company: Optional[ReferenceObject]
    supervisor: Optional[ReferenceObject]
    termination: Termination
    updated_at: datetime
    _meta: Meta

    @classmethod
    def from_obj(cls: Type[T], obj: Employment) -> T:
        return cls(
            id=obj.id,
            status=obj.status,
            weekly_working_hours=obj.weekly_working_hours,
            full_time_weekly_working_hours=obj.full_time_weekly_working_hours,
            probation_end_date=obj.probation_end_date,
            employment_end_date=obj.employment_end_date,
            employment_start_date=obj.employment_start_date,
            type=obj.type,
            contract_end_date=obj.contract_end_date,
            cost_centers=[SyncCostCenter.from_obj(cc) for cc in obj.cost_centers or []],
            created_at=obj.created_at,
            legal_entity=(
                LegalEntity.from_obj(obj.legal_entity) if obj.legal_entity else None
            ),
            office=obj.office,
            org_units=(
                [OrgUnit.from_obj(ou) for ou in obj.org_units]
                if obj.org_units
                else None
            ),
            person=Person.from_obj(obj.person),
            position=obj.position,
            sub_company=obj.sub_company,
            supervisor=obj.supervisor,
            termination=obj.termination,
            updated_at=obj.updated_at,
            _meta=obj._meta,
        )
