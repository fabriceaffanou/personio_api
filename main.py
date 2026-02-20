from typing import Any

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.PersonioClient.factory import create_personio_client
from src.PersonioSyncService.factory import create_personio_sync_service
from src.PersonioSyncService.custom_serializer import to_dict

app = FastAPI(
    root_path="/microservice/personio",
    title="Personio microservice",
    description="API to fetch and sync Personio persons.")

security = HTTPBasic()


@app.get("/sync-persons")
def get_sync_persons(
    credentials: HTTPBasicCredentials = Depends(security),
) -> list[dict[str, Any]]:
    """
    Fetch Personio persons and return the list of sync persons.
    Provide credentials via HTTP Basic Auth (client_id as username, client_secret as password).
    """
    client_id = credentials.username
    client_secret = credentials.password
    try:
        client = create_personio_client(client_id=client_id, client_secret=client_secret)
        sync_service = create_personio_sync_service(client)
        sync_persons = sync_service.get_sync_persons()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Personio sync failed: {e!s}")
    return to_dict(sync_persons)

@app.get("/health")
def get_health():
    return {"status": "ok"}