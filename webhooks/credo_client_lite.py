import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv


class CredoClientLite:
    """Lightweight client for interacting with the Credo AI webhook API."""

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
        self.session.headers.update({
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json"
        })

    def __repr__(self) -> str:
        """Return a short string summary of this client instance."""
        return f"CredoClientLite(tenant='{self.tenant}', server='{self.server}')"

    @classmethod
    def load_config(cls, config_path: str = ".env") -> "CredoClientLite":
        """Load required client configuration from a .env file.

        Reads credentials and configuration settings from the given `.env` file
        and returns a configured instance of `CredoClientLite`.

        Required environment variables:
            - API_KEY
            - TENANT
            - WEBHOOK_URL

        Optional:
            - SERVER (defaults to https://api.credo.ai)

        Args:
            config_path (str): Path to the .env file to read. Defaults to `.env`.

        Returns:
            CredoClientLite: A configured client instance.

        Raises:
            FileNotFoundError: If the .env file is missing.
        """
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
        """Authenticate with the Credo AI API using an API token.

        Exchanges your API token for a short-lived bearer token used for
        authenticated API calls. If successful, the token is stored in the
        session headers and reused for future requests.

        Returns:
            bool: True if authentication was successful, otherwise False.

        Logs:
            - Prints a message if authentication fails or if no token is returned.
        """
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
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
    ) -> Optional[Dict[str, Any]]:
        """Internal helper for making authenticated API requests.

        Sends an HTTP request to the specified endpoint using the given method
        and optional request body. The base URL and authorization token are
        automatically applied.

        Args:
            method (str): HTTP method to use (GET, POST, PATCH, DELETE).
            endpoint (str): Path under the /api/v2/{tenant} route.
            data (Optional[Dict]): Optional JSON body for POST/PATCH requests.

        Returns:
            Optional[Dict[str, Any]]: The parsed JSON response, or None on failure
            or if the response body is empty (e.g. 204 No Content).

        Logs:
            - Prints request failures or missing authentication.
        """
        if not self.auth_token:
            print("Error: Not authenticated. Call `authenticate()` first.")
            return None

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(method=method, url=url, json=data)
            response.raise_for_status()

            if response.status_code == 204 or not response.text.strip():
                return {}

            return response.json()
        except requests.RequestException as exc:
            print(f"Request failed: {exc}")
            return None

    def get_webhooks(self) -> Optional[Dict[str, Any]]:
        """Retrieve all configured webhooks for the current tenant.

        Returns:
            Optional[Dict[str, Any]]: A list of webhook objects if successful,
            otherwise None.

        Example usage:
            webhooks = client.get_webhooks()
            for webhook in webhooks["data"]:
                print(webhook["id"], webhook["attributes"]["url"])
        """
        return self._make_request("GET", "webhooks")

    def get_webhook(self, webhook_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve details about a specific webhook by ID.

        Sends a GET request to the Credo AI API to fetch the current configuration and
        metadata for a preexisting webhook. This includes the delivery URL, event
        types, environment, authentication settings, and webhook metadata.

        The response can help verify that the webhook was configured correctly, or be used
        as the basis for a future update.

        Args:
            webhook_id (str): The ID of the webhook to retrieve.

        Returns:
            Optional[Dict[str, Any]]: A detailed response containing webhook metadata.
        """
        return self._make_request("GET", f"webhooks/{webhook_id}")

    def create_webhook(self, webhook_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a webhook in the Credo AI platform.

        Register a webhook with the Credo AI API for a specified set of events. You must
        provide the target delivery URL, a list of event types, and specify the
        authentication method to be used. Additional fields such as environment or event
        type modifiers can be optionally provided to control how events are delivered.

        Args:
            webhook_data (dict): Webhook payload to send to the API.

        Returns:
            Optional[Dict[str, Any]]: Full response including webhook ID and config if successful.

        Required Fields:
            - description (str): A human-readable description of the webhook.
            - event_types (List[str]): Events that will trigger this webhook.
            - url (str): Callback URL for webhook delivery.
            - authentication_method (str): One of `"none"` or `"o_auth"`.

        Conditionally Required (if using `"o_auth"`):
            - authentication_payload
            - authentication_payload_type
            - authentication_server

        Optional Fields:
            - event_type_prefix
            - event_type_suffix
            - environment
        """
        return self._make_request("POST", "webhooks", data=webhook_data)

    def update_webhook(self, webhook_id: str, webhook_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing webhook's configuration.

        Accepts a full or partial payload and sends a PATCH request to the API
        to update an existing webhook resource.

        Args:
            webhook_id (str): The ID of the webhook to update.
            webhook_data (dict): JSON:API-style payload with updated fields.

        Returns:
            Optional[Dict[str, Any]]: API response if the update succeeds, otherwise None.

        Notes:
            - Must include the `"id"` and `"type": "webhook"` fields in the payload root.
            - Only fields present in `attributes` will be updated.
        """
        return self._make_request("PATCH", f"webhooks/{webhook_id}", data=webhook_data)

    def delete_webhook(self, webhook_id: str) -> bool:
        """Delete a webhook from the tenant by ID.

        Sends a DELETE request to remove the webhook from the system.

        Args:
            webhook_id (str): ID of the webhook to delete.

        Returns:
            bool: True if the webhook was successfully deleted, otherwise False.
        """
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
