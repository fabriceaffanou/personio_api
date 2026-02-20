import logging
from typing import List
from PersonioClient.Data import CostCenter
from PersonioClient.Data.LegalEntity import LegalEntity
from PersonioClient.Data.Person import Person
from PersonioClient.Data.Workplace import Workplace
from PersonioClient.i_personio_client import IPersonioClient
from PersonioSyncService.Data.SyncPerson import SyncPerson
from PersonioSyncService.Data.SyncEmployment import SyncEmployment
from PersonioSyncService.employment_mapper import build_sync_employment


def build_sync_person(
    person: Person,
    personio_client: IPersonioClient,
    cost_centers: List[CostCenter],
    legal_entities: List[LegalEntity],
    workplaces: List[Workplace],
) -> SyncPerson:
    """
    Docstring for build_sync_person

    :param workplaces:
    :param person: Description
    :param personio_client: Description
    :param cost_centers: Description
    :param legal_entities: Description
    :return: Description
    :rtype: SyncPerson
    """
    employments = personio_client.get_employments(person.id)

    sync_employments: List[SyncEmployment] = [
        build_sync_employment(
            employment=e,
            person=person,
            personio_client=personio_client,
            cost_centers=cost_centers,
            legal_entities=legal_entities,
            workplaces=workplaces,
        )
        for e in employments
    ]
    company_employee_id = ""
    for attribute in person.custom_attributes:
        if attribute.id == "company_employee_id":
            company_employee_id = attribute.value

    if not company_employee_id:
        logging.warning(
            f"No 'company_employee_id' found for person {person.id}, continuing with empty string."
        )

    return SyncPerson(
        id=person.id,
        company_employee_id=company_employee_id,
        email=person.email,
        created_at=person.created_at,
        updated_at=person.updated_at,
        first_name=person.first_name,
        last_name=person.last_name,
        preferred_name=person.preferred_name,
        gender=person.gender,
        profile_picture=person.profile_picture,
        status=person.status,
        custom_attributes=person.custom_attributes,
        employments=sync_employments,
        meta=person._meta,
    )
