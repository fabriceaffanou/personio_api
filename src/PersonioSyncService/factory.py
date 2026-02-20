from PersonioClient.i_personio_client import IPersonioClient
from PersonioSyncService.i_personio_sync_service import IPersonioSyncService
from PersonioSyncService.personio_sync_service import _PersonioSyncService


def create_personio_sync_service(
    personio_client: IPersonioClient,
) -> IPersonioSyncService:
    return _PersonioSyncService(personio_client)
