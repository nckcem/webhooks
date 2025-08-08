import os
import json
import time
import logging
from pathlib import Path
from typing import Any, Self

import requests
from dotenv import load_dotenv

logger = logging.getLogger("CredoClientLite")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("webhooks.log", mode="a", encoding="utf-8")
console_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def _log_event(method: str, endpoint: str, status: int, duration: float, label: str) -> None:
    logger.info(f"[{method}] {endpoint} - {status} ({int(duration)}ms) {label}")


class CredoClientLite:
    """Lightweight client for interacting with the Credo AI webhook API."""

    def __init__(
        self,
        api_key: str,
        tenant: str,
        webhook_url: str,
        server: str = "https://api.credo.ai",
    ) -> None:
        self.api_key = api_key
        self.tenant = tenant
        self.webhook_url = webhook_url
        self.server = server.rstrip("/")
        self.base_url = f"{self.server}/api/v2/{self.tenant}"
        self.auth_token: str | None = None

        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json"
        })

    def __repr__(self) -> str:
        return f"CredoClientLite(tenant='{self.tenant}', server='{self.server}')"

    @classmethod
    def load_config(cls, config_path: str = ".env") -> Self:
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
        auth_payload = {"api_token": self.api_key, "tenant": self.tenant}

        try:
            response: requests.Response = self.session.post(
                "https://api.credo.ai/auth/exchange", json=auth_payload
            )
            response.raise_for_status()
            token = response.json().get("access_token")
            if token:
                self.auth_token = token
                self.session.headers["Authorization"] = f"Bearer {token}"
                logger.info("Authenticated with Credo AI.")
                return True
            logger.warning("Authentication succeeded but no token returned.")
        except requests.RequestException as exc:
            logger.error(f"Authentication failed: {exc}")
        return False

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        log_label: str = ""
    ) -> dict[str, Any] | None:
        if not self.auth_token:
            logger.error("Not authenticated. Call `authenticate()` first.")
            return None

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        start = time.time()
        status = 500
        try:
            response: requests.Response = self.session.request(method=method, url=url, json=data)
            duration = (time.time() - start) * 1000
            status = response.status_code
            _log_event(method, endpoint, status, duration, log_label or "Request")

            if status == 204 or not response.text.strip():
                return {}

            return response.json()
        except requests.RequestException as exc:
            duration = (time.time() - start) * 1000
            _log_event(method, endpoint, status, duration, log_label or "Request failed")
            logger.error(f"Request exception: {exc}")
            return None

    def get_webhooks(self) -> dict[str, Any] | None:
        return self._make_request("GET", "webhooks", log_label="Get all webhooks")

    def get_webhook(self, webhook_id: str) -> dict[str, Any] | None:
        response = self._make_request("GET", f"webhooks/{webhook_id}", log_label="Get webhook")
        if response:
            logger.info("Webhook config:\n" + json.dumps(response, indent=2))
        return response

    def create_webhook(self, webhook_data: dict[str, Any]) -> dict[str, Any] | None:
        return self._make_request("POST", "webhooks", data=webhook_data, log_label="Create webhook")

    def update_webhook(self, webhook_id: str, webhook_data: dict[str, Any]) -> dict[str, Any] | None:
        return self._make_request("PATCH", f"webhooks/{webhook_id}", data=webhook_data, log_label="Update webhook")

    def delete_webhook(self, webhook_id: str) -> bool:
        result = self._make_request("DELETE", f"webhooks/{webhook_id}", log_label="Delete webhook")
        return result is not None


if __name__ == "__main__":
    client = CredoClientLite.load_config()

    if client.authenticate():
        client.get_webhooks()
    else:
        logger.error("Authentication failed.")
