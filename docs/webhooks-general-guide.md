<!-- omit in toc -->
# Webhooks General Guide

<!-- omit in toc -->
## Table of Contents
<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [1. About Webhooks](#1-about-webhooks)
- [2. Testing Webhooks (Quick Flow)](#2-testing-webhooks-quick-flow)
- [3. Configuring Webhooks](#3-configuring-webhooks)
  - [3.1 Example `POST` Request to Create a Webhook](#31-example-post-request-to-create-a-webhook)
  - [3.2 Webhook Configuration Example (OAuth)](#32-webhook-configuration-example-oauth)
  - [3.3 Webhook Attribute Reference](#33-webhook-attribute-reference)
- [4. Event Types](#4-event-types)
  - [4.1 Use Case Metadata Updates](#41-use-case-metadata-updates)
    - [4.1.1 Supported Metadata Fields](#411-supported-metadata-fields)
    - [4.1.2 Example Payload](#412-example-payload)
  - [4.2 Use Case Custom Field Updates](#42-use-case-custom-field-updates)
    - [4.2.1 Example Payload](#421-example-payload)
  - [4.3 Use Case Review Events](#43-use-case-review-events)
    - [4.3.1 Review Comment Added](#431-review-comment-added)
    - [4.3.2 Use Case Review Status Updated](#432-use-case-review-status-updated)
  - [4.4 Use Case Review Task Events](#44-use-case-review-task-events)
    - [4.4.1 Review Task Status Updated](#441-review-task-status-updated)
    - [4.4.2 Review Task Deleted](#442-review-task-deleted)
- [5. Testing Configured Webhooks](#5-testing-configured-webhooks)

<!-- TOC end -->

<!-- TOC --><a name="1-about-webhooks"></a>
## 1. About Webhooks

Credo AI supports outbound webhooks, enabling customers and third parties to receive real-time updates about events occurring within the platform.

Instead of polling the API to check for new data, webhooks push relevant updates to a configured URL endpoint as soon as events occur. This improves efficiency, reduces overhead, and enables timely automation across integrated systems.

**Typical use cases include:**

* Tracking changes to use cases
* Receiving new task assignments
* Monitoring review status updates


<!-- TOC --><a name="2-testing-webhooks-quick-flow"></a>
## 2. Testing Webhooks (Quick Flow)

1. **Generate a listener URL** using your own event server, or a tool like [Svix Play](https://app.svix.com/play).
2. **Create a webhook** via a `POST` request (e.g., in Postman or using the `CredoClientLite` class).
3. **Trigger events** in the Credo AI platform that match your subscribed `event_types`.
4. **Inspect payloads** received at your webhook URL via your server logs or Svix dashboard.

<!-- TOC --><a name="3-configuring-webhooks"></a>
## 3. Configuring Webhooks

> *Note: This guide assumes familiarity with the Credo AI API and authenticated access via an API key.*

You can manage webhooks via the Credo AI API using the `/webhooks` endpoint. Each webhook configuration must include:

* `url`: Destination server to receive event payloads
* `event_types`: List of event types to subscribe to
* Optional authentication settings:

  * `authentication_method`
  * `authentication_payload`
  * `authentication_payload_type`
  * `authentication_server`


<!-- TOC --><a name="31-example-post-request-to-create-a-webhook"></a>
### 3.1 Example `POST` Request to Create a Webhook

```http
POST https://api.credo.ai/api/v2/<your-tenant>/webhooks
Content-Type: application/vnd.api+json
Authorization: Bearer <your-token>

{
  "data": {
    "type": "webhook",
    "attributes": {
      "description": "Test webhook",
      "url": "https://your-event-server.com/webhook",
      "event_types": ["use_case_review_status_updated"],
      "event_type_prefix": "CredoAI",
      "event_type_suffix": "v1",
      "environment": "production",
      "authentication_method": "none"
    }
  }
}
```

**Programmatic example using `CredoClientLite`:**

```python
from app.credo_client_lite import CredoClientLite

client = CredoClientLite.load_config()
client.authenticate()

payload = {
    "data": {
        "type": "webhook",
        "attributes": {
            "description": "Test webhook",
            "url": client.webhook_url,
            "event_types": ["use_case_review_status_updated"],
            "environment": "production",
            "authentication_method": "none"
        }
    }
}

client.create_webhook(payload)
```

<!-- TOC --><a name="32-webhook-configuration-example-oauth"></a>
### 3.2 Webhook Configuration Example (OAuth)

```json
{
  "data": {
    "attributes": {
      "description": "Webhook for order creation events",
      "event_types": [
        "use_case_review_status_updated",
        "use_case_custom_field_updated"
      ],
      "url": "https://example.com/webhooks/orders",
      "event_type_prefix": "CredoAI",
      "event_type_suffix": "v1",
      "environment": "production",
      "authentication_method": "o_auth",
      "authentication_payload": {
        "key": "secret_key_value"
      },
      "authentication_payload_type": "application/json",
      "authentication_server": "https://auth.example.com"
    }
  }
}
```


<!-- TOC --><a name="33-webhook-attribute-reference"></a>
### 3.3 Webhook Attribute Reference

| Field                         | Required?      | Description                                                                       |
| ----------------------------- | -------------- | --------------------------------------------------------------------------------- |
| `description`                 | ✅ Yes          | A human-readable description of the webhook                                       |
| `event_types`                 | ✅ Yes          | List of event types the webhook will listen for                                   |
| `url`                         | ✅ Yes          | The endpoint the webhook will call when triggered                                 |
| `event_type_prefix`           | ❌ No           | Prefix for the `type` field in the webhook payload                                |
| `event_type_suffix`           | ❌ No           | Suffix for the `type` field in the webhook payload                                |
| `environment`                 | ❌ No           | Deployment environment (e.g., `production`, `qa`, `staging`)                      |
| `authentication_method`       | ✅ Yes          | Authentication method used; options: `none`, `o_auth`                             |
| `authentication_payload`      | 🔶 Conditional | Required if `authentication_method` is `o_auth`                                   |
| `authentication_payload_type` | 🔶 Conditional | Required if `authentication_method` is `o_auth`; e.g., `application/json`         |
| `authentication_server`       | 🔶 Conditional | Required if `authentication_method` is `o_auth`; specifies the OAuth token server |

**Legend:**

* ✅ **Required**
* ❌ **Optional**
* 🔶 **Conditionally required** — only if `authentication_method = o_auth`

---

<!-- TOC --><a name="4-event-types"></a>
## 4. Event Types

Credo AI webhooks support a wide variety of event types, allowing external systems to respond to updates in near real-time.


<!-- TOC --><a name="41-use-case-metadata-updates"></a>
### 4.1 Use Case Metadata Updates

**Format:**

```
use_case_<metadata_field>_updated
```

Triggered when a specific metadata field on a use case is modified.

<!-- TOC --><a name="411-supported-metadata-fields"></a>
#### 4.1.1 Supported Metadata Fields

| Field                 | Event Type                             | Description                             |
| --------------------- | -------------------------------------- | --------------------------------------- |
| `governance_status`   | `use_case_governance_status_updated`   | Governance lifecycle stage 🛑 DEPRECATED |
| `risk_category_level` | `use_case_risk_category_level_updated` | Risk level or tier assigned             |
| `name`                | `use_case_name_updated`                | Use case name                           |
| `icon`                | `use_case_icon_updated`                | Visual icon for the use case            |
| `description`         | `use_case_description_updated`         | Use case description                    |
| `industries`          | `use_case_industries_updated`          | Tagged industries                       |
| `regions`             | `use_case_regions_updated`             | Geographic scope                        |
| `ai_type`             | `use_case_ai_type_updated`             | Type of AI used                         |
| `is_vendor`           | `use_case_is_vendor_updated`           | Whether it’s a vendor-provided use case |
| `questionnaire_ids`   | `use_case_questionnaire_ids_updated`   | Associated questionnaire IDs            |

<!-- TOC --><a name="412-example-payload"></a>
#### 4.1.2 Example Payload

```json
{
  "data":{
    "status":"in_progress",
    "user":{
        "email":"cemenenkoff@credo.ai",
        "role":"admin",
        "job":null,
        "userId":"YNYykoSUoCxTtHtCrsmybE",
        "nickname":"Nick",
        "familyName":"Cemenenkoff",
        "givenName":"Nick"
    },
    "eventType":"use_case_review_status_updated",
    "useCaseId":"SeFqMYkJTSqe6fXgL7GryZ",
    "reviewId":"L7BNWLapGiuMQVNEwuS49N"
  },
  "type":"CredoAI.use_case_review_status_updated.v1",
  "time":"2025-08-08T05:56:32.136590Z",
  "source":"CredoAI",
  "subject":"use_case_review_status_updated"
}
```

---

<!-- TOC --><a name="42-use-case-custom-field-updates"></a>
### 4.2 Use Case Custom Field Updates

**Event Type:** `use_case_custom_field_updated`

Triggered when a custom field is created, updated, or removed from a use case.

<!-- TOC --><a name="421-example-payload"></a>
#### 4.2.1 Example Payload

```json
{
  "data": {
    "customFieldId": "qPSHywBSDF9HXwBVvrwKJ2",
    "customFieldName": "Target Review Date",
    "customFieldType": "number",
    "useCaseId": "QHG9s995aVztB6Xc3caXyW",
    "user": {
      "email": "steven+1@credo.ai",
      "givenName": "Steven",
      "role": "admin"
    },
    "value": "05/23/2024"
  },
  "type": "CredoAI.use_case_custom_field_updated"
}
```

---

<!-- TOC --><a name="43-use-case-review-events"></a>
### 4.3 Use Case Review Events

<!-- TOC --><a name="431-review-comment-added"></a>
#### 4.3.1 Review Comment Added

**Event Type:** `use_case_review_comment`
Triggered when a comment is added to a review or a reply is made.

```json
{
  "data": {
    "comment": "Hello @[John Doe](users:MMC8qELwNoq9V27Y2cvqHf)",
    "reviewId": "yzbEcKRh3M6xNXYmuTownS",
    "taggedUsers": [
      {
        "user": "John Doe",
        "user_id": "MMC8qELwNoq9V27Y2cvqHf"
      }
    ],
    "useCaseId": "QHG9s995aVztB6Xc3caXyW"
  },
  "type": "CredoAI.use_case_review_comment"
}
```

<!-- TOC --><a name="432-use-case-review-status-updated"></a>
#### 4.3.2 Use Case Review Status Updated

**Event Type:** `use_case_review_status_updated`
Triggered when a review is created or its status changes.

```json
{
  "data": {
    "reviewId": "pu7BDgxfVnK4RTQyb88uL",
    "status": "in_progress",
    "useCaseId": "ZiSPid3wLeXWTe4VTRjbq9",
    "user": {
      "email": "steven@credo.ai",
      "userId": "FSZqZLT8eFUUp53uTM6Ref"
    }
  },
  "type": "CredoAI.use_case_review_status_updated.v1"
}
```

---

<!-- TOC --><a name="44-use-case-review-task-events"></a>
### 4.4 Use Case Review Task Events

<!-- TOC --><a name="441-review-task-status-updated"></a>
#### 4.4.1 Review Task Status Updated

**Event Type:** `use_case_review_task_status_updated`
Triggered when the status or sub-status of a review task is updated.

```json
{
  "data": {
    "assignedUserId": "FSZqZLT8eFUUp53uTM6Ref",
    "assignerId": "FSZqZLT8eFUUp53uTM6Ref",
    "reviewId": "pu7BDgxfVnK4RTQyb88uL",
    "status": "done",
    "subStatus": "approve",
    "useCaseId": "ZiSPid3wLeXWTe4VTRjbq9",
    "user": {
      "email": "steven@credo.ai",
      "userId": "FSZqZLT8eFUUp53uTM6Ref"
    }
  },
  "type": "CredoAI.use_case_review_task_status_updated.v1"
}
```


<!-- TOC --><a name="442-review-task-deleted"></a>
#### 4.4.2 Review Task Deleted

**Event Type:** `use_case_review_task_deleted`
Triggered when a review task is removed from a use case.

```json
{
  "data": {
    "assignedUserId": "FSZqZLT8eFUUp53uTM6Ref",
    "assignerId": "FSZqZLT8eFUUp53uTM6Ref",
    "reviewId": "pu7BDgxfVnK4RTQyb88uL",
    "useCaseId": "ZiSPid3wLeXWTe4VTRjbq9",
    "user": {
      "email": "steven@credo.ai",
      "userId": "FSZqZLT8eFUUp53uTM6Ref"
    }
  },
  "type": "CredoAI.use_case_review_task_deleted.v1"
}
```

<!-- TOC --><a name="5-testing-configured-webhooks"></a>
## 5. Testing Configured Webhooks
Check out the [webhooks-testing-guide.md](/docs/webhooks-testing-guide.md)