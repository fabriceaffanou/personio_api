from abc import ABC
from typing import List

from PersonioSyncService.Data.SyncPerson import SyncPerson


class IPersonioSyncService(ABC):

    def get_sync_persons(self) -> List[SyncPerson]:
        pass
