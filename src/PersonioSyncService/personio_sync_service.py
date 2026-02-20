from PersonioSyncService.Data.SyncPerson import SyncPerson
from typing import List

from PersonioSyncService.i_personio_sync_service import IPersonioSyncService
from PersonioSyncService.person_mapper import build_sync_person
from PersonioClient.i_personio_client import IPersonioClient


class _PersonioSyncService(IPersonioSyncService):
    def __init__(self, personio_client: IPersonioClient):
        self.client = personio_client

    def get_sync_persons(self) -> List[SyncPerson]:
        persons = self.client.get_persons()
        cost_centers = self.client.get_cost_centers()
        legal_entities = self.client.get_legal_entities()
        workplaces = self.client.get_workplaces()
        
        

        return [
            build_sync_person(
                person=person,
                personio_client=self.client,
                cost_centers=cost_centers,
                legal_entities=legal_entities,
                workplaces=workplaces,
            )
            for person in persons
        ]
