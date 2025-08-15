<!-- omit in toc -->
# Webhooks General Guide

<!-- omit in toc -->
## Table of Contents
[TOC]

## 1. About Webhooks

Webhooks allow customers and third parties to monitor specific events of interest within the Credo AI platform, enabling automated data transfers to your server as events occur.

Utilizing webhooks eliminates the need for repetitive API polling to verify data presence. Once configured, webhooks ensure timely data delivery, eliminating the need for further intervention.

Webhooks can be effectively employed to track updates to use cases, new task assignments, and status updates for reviews, enhancing operational efficiency and responsiveness.


## 2. Testing Webhooks (Quick Flow)

1. **Generate a listener URL** using your own event server, or a tool like [Svix Play](https://app.svix.com/play).
2. **Create a webhook** via a `POST` request (e.g., in Postman or using the `CredoClientLite` class).
3. **Trigger events** in the Credo AI platform that match your subscribed `event_types`.
4. **Inspect payloads** received at your webhook URL via your server logs or Svix dashboard.

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
from src.app.credo_client_lite import CredoClientLite

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

## 4. Event Types

Credo AI webhooks support a wide variety of event types, allowing external systems to respond to updates in near real-time.

### 4.1 Event Types Overview

| Application Event | Webhook Event | Status | Notes |
| --- | --- | --- | --- |
| `:use_case_updated` | `use_case_{field_name}_updated` | Active | Generates dynamic event names based on the changed field |
| `use_case_risk_classification_level_updated` | | Hard Deprecated | |
| | `use_case_risk_category_level_updated` | Active | Replaces Hard Deprecated `use_case_risk_classification_level_updated` |
| `:task_created` | `use_case_review_task_status_updated` | Active | When task.type == `:use_case_review` |
| `:task_updated` | | | |
| `:task_deleted` | `use_case_review_task_deleted` | Active | When task.type == `:use_case_review` |
| `:use_case_review_created` | `use_case_review_status_updated` | Active | |
| `:use_case_review_closed` | | | |
| `:use_case_review_action_updated` | `use_case_review_comment` | Soft Deprecated | Only when action.type == `:comment` |
| `:use_case_review_action_created` | | | |
| `:entity_custom_field_deleted` | `use_case_custom_field_updated` | Active | |
| `:entity_custom_field_updated` | | | |
| `:comment_created` | `use_case_comment` | Active | Replaces Soft-Deprecated `use_case_review_comment` |
| | `use_case_review_comment` | Soft Deprecated | Duplicate emission for backward compatibility |
| `:comment_updated` | `use_case_comment` | Active | Replaces Soft-Deprecated `use_case_review_comment` |
| | `use_case_review_comment` | Soft Deprecated | Duplicate emission for backward compatibility |


### 4.2 Use Case Metadata Updates

**Format:**

```
use_case_<metadata_field>_updated
```

Triggered when a specific metadata field on a use case is modified.

#### 4.2.1 Supported Metadata Fields

| Field                 | Event Type                             | Description                             |
| --------------------- | -------------------------------------- | --------------------------------------- |
| `governance_status`   | `use_case_governance_status_updated`   | Governance lifecycle stage 🛑 **DEPRECATED** |
| `risk_category_level` | `use_case_risk_category_level_updated` | Risk level or tier assigned             |
| `name`                | `use_case_name_updated`                | Use case name                           |
| `icon`                | `use_case_icon_updated`                | Visual icon for the use case            |
| `description`         | `use_case_description_updated`         | Use case description                    |
| `industries`          | `use_case_industries_updated`          | Tagged industries                       |
| `regions`             | `use_case_regions_updated`             | Geographic scope                        |
| `ai_type`             | `use_case_ai_type_updated`             | Type of AI used                         |
| `is_vendor`           | `use_case_is_vendor_updated`           | Whether it’s a vendor-provided use case |
| `questionnaire_ids`   | `use_case_questionnaire_ids_updated`   | Associated questionnaire IDs            |

#### 4.2.2 Example Payload

```json
{
  "data": {
    "changedFieldName": "governance_status",
    "useCaseId": "d8zdKJNgwCgKmvN8QkSQ2H",
    "user": {
      "email": "steven+1@credo.ai",
      "familyName": "Barber",
      "givenName": "Steven",
      "job": null,
      "nickname": "Steven",
      "role": "admin",
      "userId": "G7kYiogzZE4Zxt2iGkhht9"
    },
    "value": 1
  },
  "source": "CredoAI",
  "subject": "governance_status_updated",
  "time": "2024-04-26T21:30:20.055675Z",
  "type": "CredoAI.use_case_governance_status_updated"
}
```

---

### 4.3 Use Case Custom Field Updates

**Event Type:** `use_case_custom_field_updated`

Triggered when a custom field is created, updated, or removed from a use case.

#### 4.3.1 Example Payload

```json
{
  "data": {
    "customFieldId": "qPSHywBSDF9HXwBVvrwKJ2",
    "customFieldName": "Target Review Date",
    "customFieldType": "number",
    "useCaseId": "QHG9s995aVztB6Xc3caXyW",
    "user": {
      "email": "steven+1@credo.ai",
      "familyName": "Barber",
      "givenName": "Steven",
      "job": "data_scientist",
      "nickname": "steven+1",
      "role": "admin",
      "userId": "TuC8qELwNoq9V27Y2cvqHf"
    },
    "value": "05/23/2024"
  },
  "source": "CredoAI",
  "subject": "cf_qPSHywBSDF9HXwBVvrwKJ2_updated",
  "time": "2024-04-23T20:35:11.840965Z",
  "type": "CredoAI.use_case_custom_field_updated"
}
```

---

### 4.4 Use Case Comment Events

#### 4.4.1 Use Case Comment

**Event Type:** `use_case_comment`

Triggers when a comment (or reply) is added or updated on a use case.

The webhook event's data payload has the following fields:

* `commentId` – the ID of the comment that was created or updated
* `threadId` – the ID of the comment thread to which the comment belongs
* `comment` – the string content of the created or updated comment
* `useCaseId` – the ID of the use case
* `resourceType` – the type of resource the comment thread is attached to (`none`, `control`, `question`, `evidence_requirement`, or `review_action`)
* `resourceId` – the ID of the resource the comment thread is attached to
* `parentQSectionId` – the ID of the questionnaire section containing the resource when `resourceType` is `question`, or null
* `parentEntityControlId` – the ID of the use case risk or compliance control containing the resource when `resourceType` is `evidence_requirement`, or null
* `parentUseCaseReview_id` – the ID of the use case review containing the resource when `resourceType` is `review_action`, or null
* `type` – the new event type `CredoAI.use_case_comment`
* `eventName` – the specific name/trigger of the event (`comment_created` or `comment_updated`)

---

### 4.5 Use Case Review Events

#### 4.5.1 Review Comment Added - DEPRECATED

**Event Type:** `use_case_review_comment` - **DEPRECATED**

> **Note:** This event type is deprecated. Use `use_case_comment` instead for new implementations.

Triggered when a comment is added to a review or a reply is made.

```json
{
  "data": {
    "actionId": "9A6DwehJSG2UBeaHuCoFcP",
    "comment": "Hello @[John Doe](users:MMC8qELwNoq9V27Y2cvqHf) ",
    "reviewId": "yzbEcKRh3M6xNXYmuTownS",
    "taggedUsers": [
      {
        "user": "John Doe",
        "user_id": "MMC8qELwNoq9V27Y2cvqHf"
      }
    ],
    "useCaseId": "QHG9s995aVztB6Xc3caXyW",
    "user": {
      "email": "steven+1@credo.ai",
      "familyName": "Barber",
      "givenName": "Steven",
      "job": "data_scientist",
      "nickname": "steven+1",
      "role": "admin",
      "userId": "TuC8qELwNoq9V27Y2cvqHf"
    }
  },
  "source": "CredoAI",
  "subject": "use_case_review_comment",
  "time": "2024-04-22T21:41:57.189315Z",
  "type": "CredoAI.use_case_review_comment"
}
```

#### 4.5.2 Use Case Review Status Updated

**Event Type:** `use_case_review_status_updated`
Triggered when a review is created or its status changes.

```json
{
  "data": {
    "reviewId": "pu7rBDgxfVnK4RTQyb88uL",
    "status": "in_progress",
    "useCaseId": "ZiSPid3wLeXWTe4VTRjbq9",
    "user": {
      "email": "steven@credo.ai",
      "familyName": "Barber",
      "givenName": "Steven",
      "job": null,
      "nickname": "steven",
      "role": "admin",
      "userId": "FSZqZLT8eFUUp53uTM6Ref"
    }
  },
  "source": "CredoAI",
  "subject": "use_case_review_status_updated",
  "time": "2024-04-30T03:45:01.621406Z",
  "type": "CredoAI.use_case_review_status_updated.v1"
}
```

---

### 4.6 Use Case Review Task Events

#### 4.6.1 Review Task Status Updated

**Event Type:** `use_case_review_task_status_updated`
Triggered when the status or sub-status of a review task is updated.

```json
{
    "data": {
        "assignedUserId": "FSZqZLT8eFUUp53uTM6Ref",
        "assignerId": "FSZqZLT8eFUUp53uTM6Ref",
        "reviewId": "pu7rBDgxfVnK4RTQyb88uL",
        "status": "done",
        "subStatus": "approve",
        "useCaseId": "ZiSPid3wLeXWTe4VTRjbq9",
        "user": {
            "email": "steven@credo.ai",
            "familyName": "Barber",
            "givenName": "Steven",
            "job": null,
            "nickname": "steven",
            "role": "admin",
            "userId": "FSZqZLT8eFUUp53uTM6Ref"
        }
    },
    "source": "CredoAI",
    "subject": "use_case_review_task_status_updated",
    "time": "2024-04-30T04:21:14.805975Z",
    "type": "CredoAI.use_case_review_task_status_updated.v1"
}
```


#### 4.6.2 Review Task Deleted

**Event Type:** `use_case_review_task_deleted`
Triggered when a review task is removed from a use case.

```json
{
    "data": {
        "assignedUserId": "FSZqZLT8eFUUp53uTM6Ref",
        "assignerId": "FSZqZLT8eFUUp53uTM6Ref",
        "reviewId": "pu7rBDgxfVnK4RTQyb88uL",
        "useCaseId": "ZiSPid3wLeXWTe4VTRjbq9",
        "user": {
            "email": "steven@credo.ai",
            "familyName": "Barber",
            "givenName": "Steven",
            "job": null,
            "nickname": "steven",
            "role": "admin",
            "userId": "FSZqZLT8eFUUp53uTM6Ref"
        }
    },
    "source": "CredoAI",
    "subject": "use_case_review_task_deleted",
    "time": "2024-04-30T04:21:19.026290Z",
    "type": "CredoAI.use_case_review_task_deleted.v1"
}
```

## 5. Testing Your Webhooks

Before relying on your webhooks, it's important that you test your configuration.

### Step 1: Configuring your test endpoint

> **Note:** If you already have an event server setup, you can test with that. Skip to Step 2 and use that as your url. Otherwise, follow Step 1 to configure a test endpoint.

1. Navigate to [Svix Playground](https://app.svix.com/play)
2. Click "Start Now"
3. Bookmark the current page, and copy the value shown. You will use this as the url when configuring your webhook in Step 2

### Step 2: Creating your webhook

Using the new url from your test endpoint or existing event server, create your webhook via the API described above. You will need to authenticate and follow similar practices to other APIs in the Credo AI API.

If you are using a test endpoint from Svix Playground, you can set `"authentication_method"` to `"none"`. Otherwise, if you are using your own event server, set the authentication information appropriately.

You can use any valid event types to test your webhook, but a good one to test with is `"use_case_governance_status_updated"`.

### Step 3: Make a change to your use case

Assuming that you set `"use_case_governance_status_updated"` as an event type, you can test by navigating to the Use Case Settings page, updating the governance status for the use case, and then changing it back.

### Step 4: View the results

If you used an existing event server, confirm that the appropriate message was received by your server. If you're using Svix Playground, return to the URL that you bookmarked in Step 1. You should see one or more new messages in the top left corner. Click on one of the messages to see the payload.

---

For more detailed testing information, check out the [webhooks-testing-guide.md](/docs/webhooks-testing-guide.md)