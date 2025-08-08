<!-- omit in toc -->
# Credo AI Webhooks Client

A lightweight Python client for managing webhooks via the Credo AI API. Supports creating, reading, updating, and deleting webhooks with minimal setup.

<!-- omit in toc -->
## Table of Contents
<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [1. Installation](#1-installation)
  - [1.1 Prerequisites](#11-prerequisites)
  - [1.2 Setup](#12-setup)
- [2. Configuration](#2-configuration)
- [3. Usage](#3-usage)
  - [3.1 Load and Authenticate](#31-load-and-authenticate)
  - [3.2 Run the Client](#32-run-the-client)
- [4. Testing CRUD Operations](#4-testing-crud-operations)
- [5. API Overview](#5-api-overview)
  - [5.1 Key Methods](#51-key-methods)
  - [5.2 Sample Payload for Create](#52-sample-payload-for-create)
- [6. Developer Tips](#6-developer-tips)
  - [6.1 Logging](#61-logging)
  - [6.2 Manual Client Instantiation](#62-manual-client-instantiation)
  - [6.3 Webhook Event Types (Examples)](#63-webhook-event-types-examples)

<!-- TOC end -->

<!-- TOC --><a name="1-installation"></a>
## 1. Installation

<!-- TOC --><a name="11-prerequisites"></a>
### 1.1 Prerequisites

* Python 3.10+
* [Poetry](https://python-poetry.org/docs/#installation)

<!-- TOC --><a name="12-setup"></a>
### 1.2 Setup

```bash
git clone <repository-url>
cd webhooks
poetry install
poetry shell
```


<!-- TOC --><a name="2-configuration"></a>
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


<!-- TOC --><a name="3-usage"></a>
## 3. Usage

<!-- TOC --><a name="31-load-and-authenticate"></a>
### 3.1 Load and Authenticate

```python
from webhooks.credo_client_lite import CredoClientLite

client = CredoClientLite.load_config()

if client.authenticate():
    print("Authenticated")
else:
    print("Authentication failed")
```

<!-- TOC --><a name="32-run-the-client"></a>
### 3.2 Run the Client

To test your setup and list all webhooks:

```bash
poetry run python webhooks/credo_client_lite.py
```


<!-- TOC --><a name="4-testing-crud-operations"></a>
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


<!-- TOC --><a name="5-api-overview"></a>
## 5. API Overview

<!-- TOC --><a name="51-key-methods"></a>
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

<!-- TOC --><a name="52-sample-payload-for-create"></a>
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


<!-- TOC --><a name="6-developer-tips"></a>
## 6. Developer Tips

<!-- TOC --><a name="61-logging"></a>
### 6.1 Logging

Logs are written to `webhooks.log` and printed to console:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

<!-- TOC --><a name="62-manual-client-instantiation"></a>
### 6.2 Manual Client Instantiation

```python
client = CredoClientLite(
    api_key="your_api_key",
    tenant="your_tenant",
    webhook_url="https://your-endpoint.com/webhook",
    server="https://api.credo.ai"
)
```

<!-- TOC --><a name="63-webhook-event-types-examples"></a>
### 6.3 Webhook Event Types (Examples)

* `use_case_governance_status_updated` 🛑 DEPRECATED
* `use_case_review_status_updated`
* `use_case_custom_field_updated`
* `use_case_review_comment`
* `use_case_review_status_updated`
* `use_case_review_task_status_updated`

For an exhaustive list, see [webhooks-general-guide.md](/docs/webhooks-general-guide.md).
