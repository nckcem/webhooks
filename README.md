# Credo AI Webhooks Client

A lightweight Python client for managing webhooks with the Credo AI API.

## Features

- **Simple Authentication**: Easy authentication using API key and tenant
- **Webhook Management**: Full CRUD operations for webhooks
- **Configuration Management**: Load settings from `.env` file
- **Error Handling**: Robust error handling and logging
- **Clean API**: Simple and intuitive interface

## Installation

This project uses Poetry for dependency management. Install dependencies with:

```bash
poetry install
```

## Configuration

Copy `env.template` to `.env` and fill in your Credo AI credentials:

```bash
cp env.template .env
```

Then edit `.env` with your actual values:

```env
# Your API key from Credo AI
API_KEY=your_api_key_here

# Your tenant identifier
TENANT=your_tenant_here

# Your webhook URL for creating webhooks
WEBHOOK_URL=https://your-domain.com/webhook

# Server configuration (optional - defaults to https://api.credo.ai)
SERVER=https://api.credo.ai
```

## Usage

### Basic Usage

```python
from webhooks.credo_client import CredoClientLite

# Load client from .env file
client = CredoClientLite.load_config()

# Authenticate with the API
if client.authenticate():
    print("Authentication successful!")

    # Get all webhooks
    webhooks = client.get_webhooks()
    if webhooks:
        print(f"Found {len(webhooks.get('data', []))} webhooks")
else:
    print("Authentication failed!")
```

### Available Methods

#### `CredoClientLite.load_config()`
Loads configuration from `.env` file and returns a `CredoClientLite` object.

#### `client.authenticate()`
Authenticates with the Credo AI API using your API key and tenant.
Returns `True` if successful, `False` otherwise.

#### `client.get_webhooks()`
Retrieves a list of all webhooks.
Returns a dictionary with webhook data or `None` if failed.

#### `client.get_webhook(webhook_id)`
Retrieves a specific webhook by ID.
Returns a dictionary with webhook data or `None` if failed.

#### `client.create_webhook(webhook_data)`
Creates a new webhook with the provided data.
Returns the created webhook object or `None` if failed.

Example webhook data:
```python
webhook_data = {
    "data": {
        "type": "webhook",
        "attributes": {
            "url": "https://your-domain.com/webhook",
            "events": ["model.created", "model.updated"]
        }
    }
}
```

#### `client.update_webhook(webhook_id, webhook_data)`
Updates an existing webhook with the provided data.
Returns the updated webhook object or `None` if failed.

#### `client.delete_webhook(webhook_id)`
Deletes a webhook by ID.
Returns `True` if successful, `False` otherwise.

## Running the Client

Run the client directly to see it in action:

```bash
poetry run python webhooks/credo_client.py
```

The client will:
- Load configuration from `.env`
- Authenticate with the API
- Retrieve and display webhooks

## API Endpoints

The client uses the following Credo AI API endpoints:

- **Authentication**: `POST https://api.credo.ai/auth/exchange`
- **List Webhooks**: `GET {base_url}/webhooks`
- **Get Webhook**: `GET {base_url}/webhooks/{id}`
- **Create Webhook**: `POST {base_url}/webhooks`
- **Update Webhook**: `PATCH {base_url}/webhooks/{id}`
- **Delete Webhook**: `DELETE {base_url}/webhooks/{id}`

Where `{base_url}` is constructed as: `{SERVER}/api/v2/{TENANT}`

## Headers

The client automatically sets the required headers:

**Before authentication:**
```
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json
```

**After authentication:**
```
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json
Authorization: Bearer <token>
```

## Error Handling

The client includes comprehensive error handling:

- **Configuration errors**: File not found, missing required values
- **Authentication errors**: Invalid credentials, network issues
- **API errors**: HTTP errors, malformed responses
- **Request errors**: Network timeouts, connection issues

## Development

### Project Structure

```
webhooks/
├── credo_client.py      # Main client implementation
├── env.template         # Configuration template
├── pyproject.toml       # Poetry configuration
└── README.md           # This file
```

### Dependencies

- `requests`: HTTP client for API communication
- `python-dotenv`: Environment variable management

## License

MIT License - see LICENSE file for details.
