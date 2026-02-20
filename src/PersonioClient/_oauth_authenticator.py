from typing import Optional
import httpx
from httpx import Client


class _OAuthAuthenticator(httpx.Auth):
    client: Client
    client_id: str
    client_secret: str
    token_cache: Optional[str] = None

    def __init__(self, client_id: str, client_secret: str, base_url: str):
        self.client = httpx.Client(base_url=base_url)
        self.client_id = client_id
        self.client_secret = client_secret

    def auth_flow(self, request):
        if self.token_cache is None:
            self.token_cache = self.acquire_token()
        request.headers["Authorization"] = f"Bearer {self.token_cache}"
        yield request

    def acquire_token(self) -> Optional[str]:
        token_payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "",
        }
        response = self.client.post("/auth/token", data=token_payload)
        return response.json()["access_token"]
