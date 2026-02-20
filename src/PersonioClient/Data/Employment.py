from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from PersonioClient.Data.Meta import Meta
from PersonioClient.Data.ReferenceObject import ReferenceObject


class EmploymentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ONBOARDING = "ONBOARDING"
    LEAVE = "LEAVE"
    UNSPECIFIED = "UNSPECIFIED"


class EmploymentType(str, Enum):
    UNSPECIFIED = "UNSPECIFIED"
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"


class TerminationType(str, Enum):
    UNSPECIFIED = "UNSPECIFIED"
    EMPLOYEE = "EMPLOYEE"
    FIRED = "FIRED"
    DEATH = "DEATH"
    CONTRACT_EXPIRED = "CONTRACT_EXPIRED"
    AGREEMENT = "AGREEMENT"
    SUB_COMPANY_SWITCH = "SUB_COMPANY_SWITCH"
    IRREVOCABLE_SUSPENSION = "IRREVOCABLE_SUSPENSION"
    CANCELLATION = "CANCELLATION"
    COLLECTIVE_AGREEMENT = "COLLECTIVE_AGREEMENT"
    SETTLEMENT_AGREEMENT = "SETTLEMENT_AGREEMENT"
    RETIREMENT = "RETIREMENT"
    COURT_SETTLEMENT = "COURT_SETTLEMENT"
    QUIT = "QUIT"


@dataclass
class EmploymentOrgUnit:
    type: str
    id: str


@dataclass
class Position:
    title: str


@dataclass
class Termination:
    last_working_date: Optional[datetime]
    reason: str
    terminated_at: Optional[datetime]
    termination_date: Optional[datetime]
    type: TerminationType


@dataclass
class EmploymentCostCenter:
    id: str
    weight: float


@dataclass
class Employment:
    id: str
    status: EmploymentStatus
    weekly_working_hours: float
    full_time_weekly_working_hours: float
    probation_end_date: Optional[datetime]
    employment_end_date: Optional[datetime]
    employment_start_date: datetime
    type: EmploymentType
    contract_end_date: Optional[datetime]
    cost_centers: List[EmploymentCostCenter]
    created_at: datetime
    legal_entity: Optional[ReferenceObject]
    office: Optional[ReferenceObject]
    org_units: Optional[List[EmploymentOrgUnit]]
    person: ReferenceObject
    position: Optional[Position]
    sub_company: Optional[ReferenceObject]
    supervisor: Optional[ReferenceObject]
    termination: Termination
    updated_at: datetime
    _meta: Meta
