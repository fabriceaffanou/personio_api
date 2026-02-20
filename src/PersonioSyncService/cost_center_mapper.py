from typing import List, Optional
from PersonioSyncService.Data.syncCostCenter import SyncCostCenter
from PersonioClient.Data.CostCenter import CostCenter
from PersonioClient.Data.Employment import EmploymentCostCenter


def build_cost_center_by_id(
    target_id: str,
    cost_centers: List[CostCenter],
    weight: float,
) -> Optional[SyncCostCenter]:
    """
    Searches cost_centre_list for target_id.
    Returns a new CostCentre object with id and found name.
    If the ID is not found, returns None.
    """
    for cost_center in cost_centers:
        if cost_center.id == target_id:
            return SyncCostCenter(
                id=cost_center.id, name=cost_center.name, weight=weight
            )
    return None


def initialize_cost_centers(
    employment_cost_centers: List[EmploymentCostCenter], cost_centers: List[CostCenter]
) -> List[SyncCostCenter]:
    """
    Docstring for initialize_cost_centers

    :param employment_cost_centers: Description
    :type employment_cost_centers: List[EmploymentCostCenter]
    :param cost_centers: Description
    :type cost_centers: List[CostCenter]
    :return: Description
    :rtype: List[CostCenter]
    """

    initialized_cost_centers: List[SyncCostCenter] = []
    for employment_cost_center in employment_cost_centers:
        cost_center = build_cost_center_by_id(
            employment_cost_center.id, cost_centers, employment_cost_center.weight
        )
        if cost_center:
            initialized_cost_centers.append(cost_center)

    return initialized_cost_centers
