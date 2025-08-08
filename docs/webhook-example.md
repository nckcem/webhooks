Here’s a simple **Flask webhook receiver** that logs incoming **Credo AI webhook** payloads. This will help you verify that your endpoint is working.

---

## ✅ Flask Webhook Receiver (Basic Version)

```python
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Optional: log incoming webhooks to a file
logging.basicConfig(filename='webhooks.log', level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    logging.info(f"Webhook received: {data}")

    # You can inspect or process event types here
    event_type = data.get('event_type')
    print(f"Received event: {event_type}")

    # Respond to Credo AI
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 🔧 How to Use This

1. **Save as `webhook_server.py`**
2. Run with:

   ```
   python webhook_server.py
   ```
3. Expose it with [ngrok](https://ngrok.com/) for testing:

   ```
   ngrok http 5000
   ```
4. Use the generated `https://xxxx.ngrok.io/webhook` as your webhook `url` when creating it via the API or Postman.

---

## 🛡️ Optional: Add Basic Authentication (if not using Svix)

If you want to restrict access:

```python
from flask import abort

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('Authorization') != 'Bearer YOUR_SECRET_TOKEN':
        abort(403)

    data = request.get_json()
    ...
```

---

Let me know if you’d like:

* A FastAPI version
* Signature verification (if Credo AI signs payloads in the future)
* Persistence to a database or file system
