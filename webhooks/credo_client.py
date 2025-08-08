import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv


class CredoClientLite:
    """Lightweight client for interacting with Credo AI's webhook API."""

    def __init__(
        self,
        api_key: str,
        tenant: str,
        webhook_url: str,
        server: str = "https://api.credo.ai",
    ):
        self.api_key = api_key
        self.tenant = tenant
        self.webhook_url = webhook_url
        self.server = server.rstrip("/")
        self.base_url = f"{self.server}/api/v2/{self.tenant}"
        self.auth_token: Optional[str] = None

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/vnd.api+json",
                "Accept": "application/vnd.api+json",
            }
        )

    def __repr__(self) -> str:
        """Return a string representation of the client."""
        return f"CredoClientLite(tenant='{self.tenant}', server='{self.server}', base_url='{self.base_url}')"

    @classmethod
    def load_config(cls, config_path: str = ".env") -> "CredoClientLite":
        """Load credentials and URLs from a .env file."""
        env_path = Path(config_path)
        if not env_path.is_file():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        load_dotenv(dotenv_path=env_path)

        api_key = os.getenv("API_KEY", "")
        tenant = os.getenv("TENANT", "")
        webhook_url = os.getenv("WEBHOOK_URL", "")
        server = os.getenv("SERVER", "https://api.credo.ai")

        return cls(api_key, tenant, webhook_url, server)

    def authenticate(self) -> bool:
        """Authenticate and store the bearer token in the session."""
        auth_payload = {"api_token": self.api_key, "tenant": self.tenant}

        try:
            response = self.session.post(
                "https://api.credo.ai/auth/exchange", json=auth_payload
            )
            response.raise_for_status()
            token = response.json().get("access_token")
            if token:
                self.auth_token = token
                self.session.headers["Authorization"] = f"Bearer {token}"
                return True
            print("Authentication succeeded but no token returned.")
        except requests.RequestException as exc:
            print(f"Authentication failed: {exc}")
        return False

    def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """Make an authenticated request to the Credo API."""
        if not self.auth_token:
            print("Error: Not authenticated. Call `authenticate()` first.")
            return None

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(method=method, url=url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            print(f"Request failed: {exc}")
            return None

    def get_webhooks(self) -> Optional[Dict[str, Any]]:
        """Retrieve all configured webhooks."""
        return self._make_request("GET", "webhooks")

    def get_webhook(self, webhook_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific webhook by ID."""
        return self._make_request("GET", f"webhooks/{webhook_id}")

    def create_webhook(self, webhook_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new webhook."""
        return self._make_request("POST", "webhooks", data=webhook_data)

    def update_webhook(
        self, webhook_id: str, webhook_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update an existing webhook."""
        return self._make_request("PATCH", f"webhooks/{webhook_id}", data=webhook_data)

    def delete_webhook(self, webhook_id: str) -> bool:
        """Delete a webhook by ID."""
        result = self._make_request("DELETE", f"webhooks/{webhook_id}")
        return result is not None


if __name__ == "__main__":
    client = CredoClientLite.load_config()

    if client.authenticate():
        print("✅ Authenticated with Credo AI.")
        webhooks = client.get_webhooks()
        if webhooks:
            print("📦 Webhooks:", webhooks)
    else:
        print("❌ Authentication failed.")
