from typing import List, Optional, Type, Any
import httpx
import marshmallow
import marshmallow_dataclass
from httpx import Client
from httpx_retries import Retry, RetryTransport
from marshmallow import Schema

from PersonioClient.Data.LegalEntity import LegalEntity
from PersonioClient.Data.Department import Department
from PersonioClient.Data.Job import Job
from PersonioClient.Data.OrgUnit import OrgUnitType
from PersonioClient.Data.Team import Team
from PersonioClient.Data.CostCenter import CostCenter
from PersonioClient.Data.Workplace import Workplace
from PersonioClient.Data.ListResponse import ListResponse
from PersonioClient.Data.Person import Person
from PersonioClient.Data.Employment import Employment
from PersonioClient.i_personio_client import IPersonioClient
from PersonioClient._oauth_authenticator import _OAuthAuthenticator


class _PersonioClient(IPersonioClient):
    client: Client
    _department_cache: dict[str, Department] = {}
    _team_cache: dict[str, Team] = {}

    def __init__(self, client_id: str, client_secret: str, base_url: str):
        super().__init__()
        self.client = httpx.Client(
            base_url=base_url,
            transport=RetryTransport(retry=Retry(total=5, backoff_factor=0.5)),
            auth=_OAuthAuthenticator(client_id, client_secret, base_url),
        )

    def get_persons(self) -> List[Person]:
        return self._paginate_endpoint(Person, "/persons")

    def get_person(self, person_id: str) -> Optional[Person]:
        response = self.client.get(f"/persons/{person_id}")
        if response.status_code == 404:
            return None
        json_response = response.json()
        try:
            return self._get_schema(Person).load(json_response)
        except Exception as e:
            raise self._try_handle_error(e, json_response, response.status_code)

    def get_employments(self, person_id: str) -> List[Employment]:
        return self._paginate_endpoint(Employment, f"/persons/{person_id}/employments")

    def get_legal_entities(self) -> List[LegalEntity]:
        return self._paginate_endpoint(LegalEntity, "/legal-entities")

    def get_team(self, team_id: str) -> Optional[Team]:
        if team_id in self._team_cache:
            return self._team_cache[team_id]
        response = self.client.get(
            f"/org-units/{team_id}?type={OrgUnitType.team.value}"
        )
        if response.status_code == 404:
            return None
        json_response = response.json()
        try:
            team = self._get_schema(Team).load(json_response)
            self._team_cache[team_id] = team
            return team
        except Exception as e:
            raise self._try_handle_error(e, json_response, response.status_code)

    def get_department(self, department_id: str) -> Optional[Department]:
        if department_id in self._department_cache:
            return self._department_cache[department_id]
        response = self.client.get(
            f"/org-units/{department_id}?type={OrgUnitType.department.value}"
        )
        if response.status_code == 404:
            return None
        json_response = response.json()
        try:
            department = self._get_schema(Department).load(json_response)
            self._department_cache[department_id] = department
            return department
        except Exception as e:
            raise self._try_handle_error(e, json_response, response.status_code)

    def get_workplaces(self) -> List[Workplace]:
        return self._paginate_endpoint(Workplace, "/workplaces", True)

    def get_cost_centers(self) -> List[CostCenter]:
        return self._paginate_endpoint(CostCenter, "/cost-centers", True)

    def get_jobs(self) -> List[Job]:
        return self._paginate_endpoint(Job, "/recruiting/jobs?limit=200", True)

    def _paginate_endpoint[T](
        self, object_class: Type[T], endpoint: str, is_beta: bool = False
    ) -> List[T]:
        if is_beta:
            headers = {"Beta": "true"}
        else:
            headers = {}

        response = self.client.get(url=endpoint, headers=headers)
        json_response = response.json()
        try:
            result = ListResponse[T](t_class=object_class, obj=json_response)
            result_list = result.data
            while result.meta.links.__contains__("next"):
                response = self.client.get(
                    url=result.meta.links["next"], headers=headers
                )
                json_response = response.json()
                result = ListResponse[T](t_class=object_class, obj=json_response)
                result_list += result.data
            return result_list
        except Exception as e:
            raise self._try_handle_error(e, json_response, response.status_code)

    @staticmethod
    def _get_schema[T](object_class: Type[T]) -> Schema:
        return marshmallow_dataclass.class_schema(object_class)(
            unknown=marshmallow.EXCLUDE
        )

    @staticmethod
    def _try_handle_error(
        e: Exception, json_response: Any, status_code: Optional[int] = None
    ) -> Exception:
        api_errors = json_response.get("errors")
        if api_errors is not None:
            return Exception(
                str(status_code)
                + " "
                + "\n".join(
                    map(
                        lambda err: err.get("title") + ": " + err.get("detail"),
                        api_errors,
                    )
                )
            )
        return e
