from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from PersonioClient.Data.ReferenceObject import ReferenceObject


@dataclass
class JobCategoryReference:
    id: str
    name: str


@dataclass
class JobDepartmentReference:
    id: str
    name: str


@dataclass
class Job:
    id: str
    name: str
    category: Optional[JobCategoryReference]
    company: ReferenceObject
    department: JobDepartmentReference
    created_at: datetime
    updated_at: datetime
