# Academic Leave Module

## Overview
A robust academic leave system for students, staff, and admins. Supports request, approval, document upload, audit trail, notifications, analytics, and admin bulk actions.

## Models
- AcademicLeaveRequest: Main leave request, status, workflow, analytics.
- AcademicLeaveApproval: Approval/rejection by staff/admin.
- AcademicLeaveDocument: Supporting documents.
- AcademicLeaveAudit: Audit trail for all actions.

## API Endpoints
- `/academic-leave/requests/` (CRUD, submit, approve, reject, upload document)
- `/academic-leave/approval/` (CRUD)
- `/academic-leave/documents/` (CRUD)
- `/academic-leave/audit/` (read-only)

## Admin Features
- List, filter, search all leave requests.
- Bulk approve/reject actions.
- View audit trail and documents.

## Notifications
- Triggers for approval/rejection (in-app, email, SMS, and push notifications via Firebase Cloud Messaging, OneSignal).
- Analytics hooks (Google Analytics, Mixpanel) for notification delivery and workflow events.

## Analytics (Planned)
- Endpoint `/academic-leave/requests/analytics/` for leave trends, usage stats, and reporting.
- Analytics hooks for user actions and workflow events.
- Webhook endpoint `/api/integration/lms/` for LMS events

## Security
- Role-based permissions (student, staff, admin).
- Confidentiality for sensitive requests.

## Testing
- Add unit/integration tests for all workflows (recommended).

## Usage
- Students submit leave requests and documents.
- Staff/admin review, approve, or reject.
- Notifications sent on status change.
- All actions logged in audit trail.

---
*For API usage, see DRF schema or browse endpoints at `/academic-leave/`.*
