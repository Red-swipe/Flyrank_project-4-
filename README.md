# FlyRank Auth API

## What This Is
FastAPI + Supabase Auth project that handles signup, login, logout, and protected routes using JWT Bearer tokens. Built with modern Python best practices and clean architecture.

## Environment Setup
Create a `.env` file in the project root with:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your anon public key
```

## How to Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## API Reference
| Method | Endpoint | Auth Required | Description | Success Code |
|--------|----------|---------------|-------------|--------------|
| POST | /auth/signup | No | Register new user | 201 |
| POST | /auth/login | No | Login and receive JWT tokens | 200 |
| POST | /auth/logout | Bearer | Sign out current user | 204 |
| GET | /public/info | No | Public welcome message | 200 |
| GET | /protected/profile | Bearer | Returns user id, email, created_at | 200 |
| GET | /protected/dashboard | Bearer | Returns welcome message and user_id | 200 |

## Status Codes Used
- **201** – Created. Returned when a new user signs up via `/auth/signup`.
- **200** – OK. Returned for successful login (`/auth/login`), public info (`/public/info`), and protected profile/dashboard routes.
- **204** – No Content. Returned when user signs out via `/auth/logout`.
- **400** – Bad Request. Returned when signup/login data is missing or invalid.
- **401** – Unauthorized. Returned when the Bearer token is missing, malformed, or invalid/expired.

## Swagger UI
Documentation automatically available at `/docs`. Interactive API explorer where you can test endpoints and view response schemas.

![Swagger UI](swagger-screenshot.png)

## Notes on Token Handling
The `verify_token` dependency extracts the Bearer token via FastAPI's `Header(None)`, then validates it using `supabase.auth.get_user(token)`. This `Depends(verify_token)` is applied to all protected routes (`/protected/profile`, `/protected/dashboard`, `/auth/logout`), while public routes (`/public/info`, `/auth/signup`, `/auth/login`) remain unauthenticated. The `Security(bearer_scheme)` wrapper is added only for Swagger UI lock icon display and does not replace the real authentication logic.