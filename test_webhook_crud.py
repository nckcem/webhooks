import json
import logging
import time
from webhooks.credo_client_lite import CredoClientLite

# --- Configure logging ---
logger = logging.getLogger("webhook_test")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("test_webhook_crud.log", mode="a")
console_handler = logging.StreamHandler()

formatter = logging.Formatter("[%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_event(method: str, endpoint: str, status: int, duration: float, label: str):
    logger.info(f"[{method}] {endpoint} - {status} ({int(duration)}ms) {label}")


def create_webhook(client: CredoClientLite) -> str:
    """Create a webhook in the Credo AI platform."""
    payload = {
        "data": {
            "type": "webhook",
            "attributes": {
                "description": "Test webhook",
                "event_types": ["use_case_governance_status_updated"],
                "url": client.webhook_url,
                "event_type_prefix": "CredoAI",
                "event_type_suffix": "v1",
                "environment": "production",
                "authentication_method": "none",
                "authentication_payload": {"key": "secret_key_value"},
                "authentication_payload_type": "application/json",
                "authentication_server": "https://auth.example.com"
            }
        }
    }

    start = time.time()
    response = client.create_webhook(payload)
    duration = (time.time() - start) * 1000

    status = response.get("status", 201 if response else 500)
    log_event("POST", "webhooks", status, duration, "Create webhook")

    if response and "data" in response:
        return response["data"]["id"]
    else:
        raise RuntimeError("Failed to create webhook")


def get_webhook(client: CredoClientLite, webhook_id: str):
    """Retrieve and print the full config of a webhook by ID."""
    start = time.time()
    response = client.get_webhook(webhook_id)
    duration = (time.time() - start) * 1000

    status = response.get("status", 200 if response else 500)
    log_event("GET", f"webhooks/{webhook_id}", status, duration, "Get webhook")

    logger.info("Webhook config:\n" + json.dumps(response, indent=2))


def update_webhook(client: CredoClientLite, webhook_id: str):
    """Update the webhook's URL and description.

    Adds a query param to the URL to simulate a changed configuration.
    This has no effect unless your receiving server interprets it.
    """
    updated_url = client.webhook_url.rstrip("/") + "?source=update-test"

    payload = {
        "data": {
            "type": "webhook",
            "id": webhook_id,
            "attributes": {
                "description": "Updated test webhook",
                "url": updated_url,
                "event_types": ["use_case_governance_status_updated"],
                "event_type_prefix": "CredoAI",
                "event_type_suffix": "v1",
                "environment": "production",
                "authentication_method": "none"
            }
        }
    }

    start = time.time()
    response = client.update_webhook(webhook_id, payload)
    duration = (time.time() - start) * 1000

    status = response.get("status", 200 if response else 500)
    log_event("PATCH", f"webhooks/{webhook_id}", status, duration, "Update webhook")


def delete_webhook(client: CredoClientLite, webhook_id: str):
    """Delete the specified webhook by ID."""
    start = time.time()
    success = client.delete_webhook(webhook_id)
    duration = (time.time() - start) * 1000

    status = 204 if success else 500
    log_event("DELETE", f"webhooks/{webhook_id}", status, duration, "Delete webhook")


if __name__ == "__main__":
    client = CredoClientLite.load_config()

    if not client.authenticate():
        logger.error("Authentication failed.")
        exit(1)

    logger.info(f"Using client: {client}")

    webhook_id = create_webhook(client)
    get_webhook(client, webhook_id)
    update_webhook(client, webhook_id)
    delete_webhook(client, webhook_id)
