TASK:
- Create `test_webhook_crud.py` that performs the following general test of this client.
    - Authenticates
    - Creates a webhook
    - Gets the newly-created webhook
    - Updates the webhook
    - Gets the newly-updated webhook
    - Deletes the webhook

SPECIFICATIONS:
- Have the test file output to an appropriately-named .log file (test_webhook_crud.log).
- Make sure the log format is extremely clear and verbose, like:
[2025-08-07 18:00:00] ✅ [POST] /webhooks - 201 Created (324ms)
Request Payload:
{
  "data": {
    "type": "webhook",
    "attributes": {
      "url": "https://example.com/hook",
      "events": ["create", "delete"]
    }
  }
}
Response:
{
  "data": {
    "id": "wh_123",
    "type": "webhook",
    "attributes": {
      "status": "active"
    }
  }
}
------------------------------------------------------------

FORMATTING:
- Ensure all messages end with punctuation unless showing a variable like: {var}
- Don't use one-letter variable names
- Use Google-style Python docstrings like:
    """Request and update a new access token for the session.

    Returns:
        Optional[str]: The new access token if successful, otherwise None.

    Logs:
        - Debug message when requesting new token
        - Exception details when token refresh fails
        - Error message when access token is not found in response
        - Info message when token is successfully refreshed
    """