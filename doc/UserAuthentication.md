# User Authentication

This project will use Bearer Authentication and JWT tokens to authenticate users.

## JWT Claims

A JWT token contains following information:

- `user_id`: The user `_id` stored in mongo database.
- `iat`: Time when token is created in unix epoch format.
- `exp`: Time when token expires in unix epoch format. By default, a token will expire after `30 days`.

**Example claim:**

```json
{
    "user_id": "61697da2a9fd362910a4a585",
    "iat": 1634956713,
    "exp": 1637552313
}
```

## User Login

User can login by sending a `POST` request to the `/login` endpoint:
```bash
curl -H "Content-Type: application/json" -X POST http://wesource-server:5000/login -d '{"email": "dummyuser", "password": "pwd"}'
```

Server will compare `email` and `password` data against database. If user exists, it will return `200 OK` with a freshly issued JWT token:
```bash
{ "jwt": "jwt-token" }
```

If user verification fails, it will return `401 Unauthorized`.

## Authentication

Certain endpoints are restricted to users who are loggined. Reequest need must include a JWT token in its `Authorization` header to access these restricted endpoints:
```bash
curl -H "Authorization: Bearer <jwt-token>" http://wesource-server:5000/restricted-resources
```
