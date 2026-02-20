from typing import List

from PersonioClient.Data.CostCenter import CostCenter
from PersonioClient.Data.Employment import Employment
from PersonioClient.Data.LegalEntity import LegalEntity
from PersonioClient.Data.Person import Person
from PersonioClient.Data.Workplace import Workplace
from PersonioClient.i_personio_client import IPersonioClient
from PersonioSyncService.Data.SyncEmployment import SyncEmployment
from PersonioSyncService.cost_center_mapper import initialize_cost_centers
from PersonioSyncService.legal_entity_mapper import build_legal_entity_by_id
from PersonioSyncService.org_units_mapper import initialize_orgs_unit_attr


def build_sync_employment(
    employment: Employment,
    person: Person,
    personio_client: IPersonioClient,
    cost_centers: List[CostCenter],
    legal_entities: List[LegalEntity],
    workplaces: List[Workplace],
) -> SyncEmployment:
    """
    Docstring for build_sync_employment

    :param workplaces:
    :param employment: Description
    :param person: Description
    :param personio_client: Description
    :param cost_centers: Description
    :param legal_entities: Description
    :return: Description
    :rtype: SyncEmployment
    """
    return SyncEmployment(
        id=employment.id,
        status=employment.status,
        weekly_working_hours=employment.weekly_working_hours,
        full_time_weekly_working_hours=employment.full_time_weekly_working_hours,
        probation_end_date=employment.probation_end_date,
        employment_end_date=employment.employment_end_date,
        employment_start_date=employment.employment_start_date,
        type=employment.type,
        contract_end_date=employment.contract_end_date,
        cost_centers=initialize_cost_centers(employment.cost_centers, cost_centers),
        created_at=employment.created_at,
        legal_entity=(
            build_legal_entity_by_id(employment.legal_entity.id, legal_entities)
            if employment.legal_entity
            else None
        ),
        office=(
            next(
                (
                    workplace.name
                    for workplace in workplaces
                    if employment.office and workplace.id == employment.office.id
                ),
                None,
            )
            if employment.office
            else None
        ),
        org_units=(
            initialize_orgs_unit_attr(employment.org_units, personio_client)
            if employment.org_units
            else None
        ),
        person=person,
        position=employment.position,
        sub_company=employment.sub_company,
        supervisor=employment.supervisor,
        termination=employment.termination,
        updated_at=employment.updated_at,
        _meta=employment._meta,
    )
