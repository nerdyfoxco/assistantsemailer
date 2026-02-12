
# Current API Contracts (v0.6)
**Status**: FROZEN / TRUTH SOURCE

## 1. Public Surface
### Auth
-   `POST /public/auth/signup`
    -   **Input**: `SignupRequest { email, password, tenant_name, agree_tos }`
    -   **Output**: `SignupResponse { user_id, tenant_id }`
    -   **Logic**: Creates Tenant + User.

## 2. Protected Surface (`/api/v1`)
### Auth
-   `POST /api/v1/auth/login` (Implied by router inclusion)
-   `POST /api/v1/auth/refresh`

### Users
-   `GET /api/v1/users/me`
-   `PATCH /api/v1/users/me`

### Work Items
-   `GET /api/v1/work-items/`
-   `POST /api/v1/work-items/{id}/resolve`

### Emails
-   `GET /api/v1/emails/`
-   `POST /api/v1/emails/send`

### Intelligence
-   `POST /api/v1/intelligence/process`
-   `POST /api/v1/intelligence/triage`

### HITL
-   `GET /api/v1/hitl/requests`
-   `POST /api/v1/hitl/requests/{id}/claim`
-   `POST /api/v1/hitl/requests/{id}/decide`

### Admin
-   `GET /api/v1/admin/tenants`
-   `PATCH /api/v1/admin/tenants/{id}`

## 3. Data Contracts (Input/Output)
-   **SignupRequest**: Strict validation on Email.
-   **HitlRequest**: Requires `context_json` (Schema loose).

## 4. Gaps & Risks
-   **Implicit Models**: Many request/response bodies are likely defined inline or in scattered endpoint files.
-   **Missing Docs**: No Swagger/OpenAPI static export found.
