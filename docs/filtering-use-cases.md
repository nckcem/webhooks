## 🔍 How to Filter Use Cases in Credo AI

This guide shows how to **retrieve specific use cases** using filters like governance stage or risk category through the Credo AI API.

---

### 🔐 1. Authentication

Before making API calls, make sure you're authenticated.
→ See [Credo AI authentication docs](https://knowledge.credo.ai/) for setup instructions.

---

### 🌐 2. Base API URL

All requests use this base format:

```
GET https://api.credo.ai/api/v2/<your-tenant>/use_cases
```

Replace `<your-tenant>` with your actual tenant ID.

---

### 📊 3. Filter Examples

#### 🟡 Use Cases in the **Intake Stage**

```http
GET /use_cases?filter[governance_status]=0
```

#### 🟢 Use Cases in the **Governance Stage**

```http
GET /use_cases?filter[governance_status]=1
```

#### 🔴 Use Cases by **Risk Category**

Default values:

* `0` = High Risk
* `1` = Medium Risk
* `2` = Low Risk
* `3` = None

Example (High-risk use cases):

```http
GET /use_cases?filter[risk_category_level]=0
```

---

### ⚙️ 4. Custom Risk Categories

If your org uses **custom risk levels**, get them here:

```http
GET /risk_categories
```

---

### 📦 5. Response Format (Simplified)

```json
{
  "data": [
    {
      "id": "use_case_id",
      "type": "use_cases",
      "attributes": {
        "name": "Use Case Name",
        "description": "...",
        "risk_category_level": "0",
        "governance_status": "1",
        ...
      }
    }
  ],
  "meta": {
    "total_count": 17
  }
}
```

✅ `meta.total_count` tells you how many use cases matched your filter.

---

### 📄 6. Pagination

If there are too many results, use pagination:

```http
GET /use_cases?sort=inserted_at&page[after]=<cursor>
```

* Use `sort=inserted_at` to avoid duplicates.
* You can also use `page[before]=<cursor>` to paginate backward.

---

### 🔗 7. Including Related Data

To include related objects like models or vendors:

```http
GET /use_cases?include=models
```

⚠️ Only works if a defined relationship exists.