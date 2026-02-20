from PersonioClient._personio_client import _PersonioClient
from PersonioClient.i_personio_client import IPersonioClient


def create_personio_client(
    client_id: str, client_secret: str, base_url: str = "https://api.personio.de/v2"
) -> IPersonioClient:
    return _PersonioClient(client_id, client_secret, base_url)
