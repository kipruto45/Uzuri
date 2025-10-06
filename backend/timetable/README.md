# Timetable Module API Documentation

## Endpoints

### Timetable
- `GET /api/timetable/timetables/` — List all timetables
- `POST /api/timetable/timetables/` — Create timetable (admin only)
- `GET /api/timetable/timetables/{id}/` — Retrieve timetable
- `PUT/PATCH /api/timetable/timetables/{id}/` — Update timetable (admin only)
- `DELETE /api/timetable/timetables/{id}/` — Delete timetable (admin only)

### Timetable Entry
- `GET /api/timetable/entries/` — List all entries
- `POST /api/timetable/entries/` — Create entry
- `GET /api/timetable/entries/{id}/` — Retrieve entry
- `PUT/PATCH /api/timetable/entries/{id}/` — Update entry
- `DELETE /api/timetable/entries/{id}/` — Delete entry

### Timetable Change Request
- `GET /api/timetable/change-requests/` — List all change requests
- `POST /api/timetable/change-requests/` — Create change request
- `POST /api/timetable/change-requests/{id}/approve/` — Approve request (admin)
- `POST /api/timetable/change-requests/{id}/reject/` — Reject request (admin)

### Timetable Audit
- `GET /api/timetable/audits/` — List all audit records (admin)

## Permissions
- Timetable: Admin only
- TimetableEntry: Authenticated users
- TimetableChangeRequest: Authenticated users (approve/reject: admin only)
- TimetableAudit: Admin only

## Notes
- All endpoints require authentication.
- Use `/swagger/` or `/redoc/` for interactive API docs.
- Bulk approve/reject available in Django admin for change requests.
- Analytics fields are available in Timetable model.
- Notification logic is pluggable (see code comments).
