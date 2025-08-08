TASK:
- Create a very simple Python client to manage webhooks for Credo AI called CredoClientLite.
- Create an example.py file that authenticates and gets a list of webhooks.

CLIENT SPECIFICATION:
- It should read the .env file and use the API_KEY and TENANT to authenticate, and it should read the relevant webhook url.
- It should have the following simple methods:
    - client = CredoClientLite.load_config()  # Returns a CredoClientLite object
    - client.authenticate()  # Returns True if successful, False otherwise
    - webhooks = client.get_webhooks()  # Returns a list of webhooks
    - webhook = client.get_webhook(webhook_id)  # Returns a webhook object
    - client.create_webhook(webhook_data)  # Returns a webhook object
    - client.update_webhook(webhook_id, webhook_data)  # Returns a webhook object
    - client.delete_webhook(webhook_id)  # Returns True if successful, False otherwise
- Please note the BASE URL is https://api.credo.ai/api/v2/credoai
- The relevant webhooks endpoints are in the swagger.json, but here they are anyway:
    - GET /webhooks
    - POST /webhooks
    - DELETE /webhooks/{id}
    - GET /webhooks/{id}
    - PATCH /webhooks/{id}
- For authentication, the relevant endpoint is:
    - POST /auth/exchange
- Please note the session headers are:
    {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
    }
- After authentication, the session headers are:
    {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
        "Authorization": "Bearer <token>",
    }
