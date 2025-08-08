from webhooks.credo_client_lite import CredoClientLite


def create_webhook(client: CredoClientLite) -> str:
    """Create a webhook and return its ID."""
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

    response = client.create_webhook(payload)
    return response["data"]["id"] if response and "data" in response else None


def update_webhook(client: CredoClientLite, webhook_id: str):
    """Update the webhook's description and URL."""
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

    client.update_webhook(webhook_id, payload)


if __name__ == "__main__":
    client = CredoClientLite.load_config()

    if not client.authenticate():
        exit("Authentication failed.")

    webhook_id = create_webhook(client)
    if webhook_id:
        client.get_webhook(webhook_id)
        update_webhook(client, webhook_id)
        client.delete_webhook(webhook_id)
    else:
        exit("Failed to create webhook.")
