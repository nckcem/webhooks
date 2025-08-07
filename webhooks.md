## 🔗 What Are Credo AI Webhooks?

Webhooks let you **automatically receive event notifications** from Credo AI when something important happens—like:

* A use case is updated
* A task is assigned
* A review status changes

This **eliminates the need to poll the API** for updates.

---

## ⚙️ How to Set Up a Webhook

### **Step 1: Choose or Create Your Event Receiver URL**

* **Option A:** Use your own event server
* **Option B:** Use [Svix Playground](https://play.svix.com/) for testing
  → Click “Start Now” → Bookmark the provided URL

---

### **Step 2: Make a POST Request to Create the Webhook**

Use Postman or your API tool to send:

```
POST https://<your-credo-api-url>/api/v2/<tenant>/webhooks
```

**Payload Example:**

```json
{
  "url": "<your-test-endpoint-url>",
  "event_types": ["use_case_governance_status_updated"],
  "authentication_type": "none"
}
```

> Use `"authentication_type": "none"` for Svix. For your own server, provide the required auth info.

---

### **Step 3: Trigger an Event in the App**

Go into the Credo AI web UI and update something like:

* Governance Status
* Custom Field
* Review Comment
* Task Status

Example:

* Update → then revert the *governance status* of a use case to trigger `use_case_governance_status_updated`

---

### **Step 4: View the Result**

* **If using Svix Playground:** go to your bookmarked URL and look at the top-left to see incoming webhook messages and payloads.
* **If using your own server:** verify the incoming POST request payloads match the subscribed events.

---

## 🧾 Supported Event Types (Examples)

| Event Type Name                       | Trigger                          |
| ------------------------------------- | -------------------------------- |
| `use_case_governance_status_updated`  | Governance status changed        |
| `use_case_review_comment`             | Review comment added             |
| `use_case_review_status_update`       | Review created or status updated |
| `use_case_review_task_status_updated` | Task status changed              |
| `use_case_review_task_deleted`        | Task deleted                     |
| `use_case_custom_field_updated`       | Custom metadata updated          |

Event type format:

* Use case metadata: `use_case_<metadata_name>_updated`
* Custom field: `use_case_custom_field_updated`

---

## ✅ Best Practices

* Always test before deploying live webhooks
* Use [Svix](https://play.svix.com/) for simple proof-of-concept
* Secure your webhook endpoint if it’s not using Svix
* Store webhook payloads for debugging/auditing

---

Let me know if you'd like a **template JSON payload**, **authentication example**, or a **code snippet to receive webhooks** (in Flask/FastAPI/etc.).
