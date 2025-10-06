# Emasomo Module: Email-based Authentication

## Custom Email Login Endpoint

- **POST** `/emasomo/login-with-email/`
  - Request: `{ "email": "user@example.com", "password": "yourpassword" }`
  - Response: `{ "token": "<auth_token>" }` on success, `{ "error": "Invalid credentials" }` on failure.

## Requirements
- Users must log in with their email and password to access emasomo features.
- All emasomo endpoints require authentication.
- Student-specific endpoints require the student role.

## Security
- Login endpoint is rate-limited to prevent brute-force attacks.
- Email verification is enforced for new signups (see Allauth settings).

## Testing
- See `tests.py` for login endpoint tests.

## Setup
- Ensure `rest_framework.authtoken` is in `INSTALLED_APPS`.
- Run `python manage.py migrate` to create token tables.

## Note
- For production, use HTTPS and strong password policies.

## Production-Readiness Checklist
- Enforce HTTPS, secure cookies, and HSTS
- Set `DEBUG = False` and configure `ALLOWED_HOSTS`
- Use strong, secret `SECRET_KEY`
- Enable CSRF and CORS protections
- Use PostgreSQL and Redis for production
- Set up error monitoring (Sentry), logging, and backups
- Use WSGI/ASGI server (gunicorn/uvicorn) behind nginx
- Automate tests and CI/CD
- Document API and onboarding

## Advanced Additions (Recommended)
- Real-time analytics dashboards
- AI-powered chatbot and support
- Mobile app or PWA integration
- Plagiarism detection
- Proctoring for online exams
- Marketplace for resources
- Parent/guardian portal
- Multi-language and accessibility
- API rate limiting and abuse monitoring
- Automated certificate generation

## Deployment Notes
- Use environment variables for all secrets and credentials
- Regularly update dependencies and monitor for vulnerabilities
- Test backup/restore procedures
- Monitor system health and performance
