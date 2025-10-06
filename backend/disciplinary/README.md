# Disciplinary module API documentation

# Endpoints
# - /api/disciplinary/cases/ [GET, POST]: List/create cases (staff/admin), view own cases (student)
# - /api/disciplinary/cases/{id}/ [GET, PUT, PATCH, DELETE]: Retrieve/update/delete case
# - /api/disciplinary/cases/{id}/add_evidence/ [POST]: Add evidence to a case
# - /api/disciplinary/cases/{id}/submit_appeal/ [POST]: Submit appeal for a case
# - /api/disciplinary/evidence/ [GET, POST]: List/add evidence
# - /api/disciplinary/hearings/ [GET, POST]: List/schedule hearings
# - /api/disciplinary/actions/ [GET, POST]: List/add actions
# - /api/disciplinary/appeals/ [GET, POST]: List/submit appeals
# - /api/disciplinary/audit/ [GET]: View audit trail (admin)
# - /api/disciplinary/notifications/ [GET]: View notifications

# Permissions
# - Students: View own cases, submit evidence/appeals
# - Staff/Admin: Manage all cases, assign, resolve, schedule hearings
# - Committee: Access assigned hearings, record outcomes

# Notifications
# - Triggered on case creation, evidence upload, appeal submission, status changes
# - Supports in-app, email, SMS, and push notifications (Firebase Cloud Messaging, OneSignal)
# - Analytics hooks (Google Analytics, Mixpanel) for notification delivery

# Analytics
# - Dashboard endpoint `/api/disciplinary/cases/analytics/` for case stats, trends, resolution rates (see views.py)
# - Analytics hooks for user actions and workflow events
# - Webhook endpoint `/api/integration/payment/` for payment events

# For more, see views.py and models.py

## Bulk Actions

### Admin Bulk Actions
- Mark selected cases as resolved (from admin list view)
- Send notification to selected cases (from admin list view)

### API Bulk Actions
- `POST /api/disciplinary/cases/bulk_resolve/` with `{ "ids": [1,2,3] }` to mark cases as resolved
- `POST /api/disciplinary/cases/bulk_notify/` with `{ "ids": [1,2,3] }` to send notifications
