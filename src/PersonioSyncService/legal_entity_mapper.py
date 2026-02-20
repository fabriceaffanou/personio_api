from typing import List, Optional
from PersonioClient.Data.LegalEntity import LegalEntity


def build_legal_entity_by_id(
    target_id: str, legal_entity_list: List[LegalEntity]
) -> Optional[LegalEntity]:
    """
    Searches cost_centre_list for target_id.
    Returns a new CostCentre object with id and found name.
    If the ID is not found, returns None.
    """
    for legal_entity in legal_entity_list:
        if legal_entity.id == target_id:
            return LegalEntity(
                id=legal_entity.id,
                status=legal_entity.status,
                valid_from=legal_entity.valid_from,
                assigned_employees=legal_entity.assigned_employees,
                country=legal_entity.country,
                name=legal_entity.name,
                type=legal_entity.type,
                registration_number=legal_entity.registration_number,
                industry_sector=legal_entity.industry_sector,
                email=legal_entity.email,
                phone=legal_entity.phone,
                address=legal_entity.address,
                contact_person=legal_entity.contact_person,
                bank_details=legal_entity.bank_details,
                mailing_address=legal_entity.mailing_address,
                _meta=legal_entity._meta,
            )
    return None
