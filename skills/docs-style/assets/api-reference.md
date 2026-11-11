# [Service or resource in sentence case] API reference

The [Resource name] API lets you create, configure, and monitor [resources].

## Base URL

All requests use the following base URL:

```text
https://api.example.com/v1
```

## Authentication

Every endpoint requires a bearer token in the `Authorization` header:

```http
Authorization: Bearer API_KEY
```

Replace *`API_KEY`* with a token generated in the console.

## [Operation in sentence case, for example: Create a customer]

`POST /customers`

Creates a customer profile and initializes default billing settings.

### Request headers

| Header | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `Authorization` | string | Yes | A bearer token that uses the `Bearer` scheme and the *`API_KEY`* placeholder. |
| `Content-Type` | string | Yes | Set to `application/json`. |
| `Idempotency-Key` | string | No | A UUID that makes retries of the same request safe. |

### Request body

The request body is a JSON object with the following fields:

| Field | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `email` | string | Yes | None | The primary contact email address. |
| `name` | string | Yes | None | The full name of the person or organization. |
| `tier` | string | No | `standard` | The service tier: `standard`, `pro`, or `enterprise`. |
| `metadata` | object | No | `{}` | Key-value pairs for custom attributes. |

Example request:

```bash
curl -X POST https://api.example.com/v1/customers \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alex@example.com",
    "name": "Alex Rivera",
    "tier": "pro",
    "metadata": { "department": "engineering" }
  }'
```

### Response

Returns `201 Created` with the customer record:

```json
{
  "id": "cust_0000001",
  "email": "alex@example.com",
  "name": "Alex Rivera",
  "tier": "pro",
  "status": "active",
  "created_at": "2026-08-25T02:00:00Z",
  "metadata": { "department": "engineering" }
}
```

### Errors

The following table lists the error responses for this endpoint:

| HTTP status | Error code | Cause | Resolution |
| :--- | :--- | :--- | :--- |
| `400 Bad Request` | `invalid_email` | The email address is malformed. | Provide an RFC 5322 email address. |
| `401 Unauthorized` | `invalid_token` | The API key is missing or expired. | Generate a new key in the console. |
| `409 Conflict` | `customer_exists` | A customer with this email already exists. | Retrieve the record with `GET /customers?email=`*`EMAIL`*. |
| `429 Too Many Requests` | `rate_limit_exceeded` | The request quota is exhausted. | Retry with exponential backoff. |
