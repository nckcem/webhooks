<!-- omit in toc -->
# Credo AI Webhooks Client

A lightweight Python client for managing webhooks via the Credo AI API. Supports creating, reading, updating, and deleting webhooks with minimal setup.

<!-- omit in toc -->
## Table of Contents
[TOC]

## 1. Installation

### 1.1 Prerequisites

* Python 3.10+
* [Poetry](https://python-poetry.org/docs/#installation)

### 1.2 Setup

```bash
git clone <repository-url>
cd webhooks
poetry install
poetry shell
```


## 2. Configuration

1. Copy the environment template:

   ```bash
   cp env.template .env
   ```

2. Edit the `.env` file:

   ```env
   API_KEY=your_credo_ai_api_key
   TENANT=your_tenant_name
   WEBHOOK_URL=https://your-webhook-endpoint.com/webhook
   SERVER=https://api.credo.ai
   ```


## 3. Usage

### 3.1 Load and Authenticate

```python
from webhooks.credo_client_lite import CredoClientLite

client = CredoClientLite.load_config()

if client.authenticate():
    print("Authenticated")
else:
    print("Authentication failed")
```

### 3.2 Run the Client

To test your setup and list all webhooks:

```bash
poetry run python webhooks/credo_client_lite.py
```


## 4. Testing CRUD Operations

Run the test script to exercise the full webhook lifecycle:

```bash
poetry run python tests/test_webhook_crud.py
```

This test will:

1. Create a webhook
2. Retrieve and print its configuration
3. Update its description and URL
4. Delete it from the system


## 5. API Overview

### 5.1 Key Methods

| Method                        | Description                       |
| ----------------------------- | --------------------------------- |
| `load_config()`               | Load settings from `.env`         |
| `authenticate()`              | Exchange API key for bearer token |
| `get_webhooks()`              | Fetch all webhooks                |
| `get_webhook(webhook_id)`     | Fetch a single webhook by ID      |
| `create_webhook(payload)`     | Create a new webhook              |
| `update_webhook(id, payload)` | Modify an existing webhook        |
| `delete_webhook(webhook_id)`  | Delete a webhook                  |

### 5.2 Sample Payload for Create

```python
payload = {
    "data": {
        "type": "webhook",
        "attributes": {
            "description": "My test webhook",
            "url": client.webhook_url,
            "event_types": ["use_case_review_status_updated"],
            "event_type_prefix": "CredoAI",
            "event_type_suffix": "v1",
            "environment": "production",
            "authentication_method": "none"
        }
    }
}

response = client.create_webhook(payload)
webhook_id = response["data"]["id"]
```


## 6. Developer Tips

### 6.1 Logging

Logs are written to `webhooks.log` and printed to console:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 6.2 Manual Client Instantiation

```python
client = CredoClientLite(
    api_key="your_api_key",
    tenant="your_tenant",
    webhook_url="https://your-endpoint.com/webhook",
    server="https://api.credo.ai"
)
```

### 6.3 Webhook Event Types (Examples)

* `use_case_governance_status_updated` 🛑 DEPRECATED
* `use_case_review_status_updated`
* `use_case_custom_field_updated`
* `use_case_review_comment`
* `use_case_review_status_updated`
* `use_case_review_task_status_updated`

For an exhaustive list, see [webhooks-general-guide.md](/docs/webhooks-general-guide.md).
