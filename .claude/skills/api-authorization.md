---
name: api-authorization
description: Secure APIs and enforce user isolation.
---

# API Authorization Enforcement

## Instructions
Protect all API endpoints.

1. **Authorization**
   - Verify JWT on every request
   - Extract authenticated user

2. **User isolation**
   - Ensure users access only their own tasks
   - Enforce ownership on CRUD operations

3. **Errors**
   - 401 for unauthenticated
   - 403 for unauthorized

---
