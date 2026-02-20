from abc import abstractmethod, ABC
from typing import List, Optional

from PersonioClient.Data.LegalEntity import LegalEntity
from PersonioClient.Data.CostCenter import CostCenter
from PersonioClient.Data.Department import Department
from PersonioClient.Data.Job import Job
from PersonioClient.Data.Team import Team
from PersonioClient.Data.Workplace import Workplace
from PersonioClient.Data.Person import Person
from PersonioClient.Data.Employment import Employment


class IPersonioClient(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_persons(self) -> List[Person]:
        pass

    @abstractmethod
    def get_person(self, person_id: str) -> Optional[Person]:
        pass

    @abstractmethod
    def get_employments(self, person_id: str) -> List[Employment]:
        pass

    @abstractmethod
    def get_legal_entities(self) -> List[LegalEntity]:
        pass

    @abstractmethod
    def get_team(self, team_id: str) -> Team:
        pass

    @abstractmethod
    def get_department(self, department_id: str) -> Department:
        pass

    @abstractmethod
    def get_workplaces(self) -> List[Workplace]:
        pass

    @abstractmethod
    def get_cost_centers(self) -> List[CostCenter]:
        pass

    @abstractmethod
    def get_jobs(self) -> List[Job]:
        pass
