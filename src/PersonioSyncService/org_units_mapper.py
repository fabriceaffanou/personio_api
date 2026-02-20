from typing import List, Optional
from PersonioClient.Data.OrgUnit import OrgUnit
from PersonioClient.Data.Employment import EmploymentOrgUnit
from PersonioClient.i_personio_client import IPersonioClient


def build_org_unit_by_id(
    org_unit_id: str, personio_client: IPersonioClient, org_unit_type: str
) -> Optional[OrgUnit]:
    """Searches org_unit_list for target_id."""

    if org_unit_type == "department":
        department = personio_client.get_department(org_unit_id)
        if department:
            return OrgUnit(
                id=department.id,
                name=department.name,
                type=department.type,
                abbreviation=department.abbreviation,
                description=department.description,
                resource_uri=department.resource_uri,
                create_time=department.create_time,
                _meta=department._meta,
            )
    elif org_unit_type == "team":
        team = personio_client.get_team(org_unit_id)
        if team:
            return OrgUnit(
                id=team.id,
                name=team.name,
                type=team.type,
                abbreviation=team.abbreviation,
                description=team.description,
                resource_uri=team.resource_uri,
                create_time=team.create_time,
                _meta=team._meta,
            )

    return None


def initialize_orgs_unit_attr(
    employment_org_units: List[EmploymentOrgUnit], personio_client: IPersonioClient
) -> List[OrgUnit]:
    """
    Docstring for initialize_orgs_unit_attr

    :param personio_client:
    :param employment_org_units: Description
    :type employment_org_units: List[EmploymentOrgUnit]
    :return: Description
    :rtype: List[OrgUnit]
    """

    initialized_org_units: List[OrgUnit] = []
    for employment_org_unit in employment_org_units:
        org_unit = build_org_unit_by_id(
            employment_org_unit.id, personio_client, employment_org_unit.type
        )
        if org_unit:
            initialized_org_units.append(org_unit)

    return initialized_org_units
