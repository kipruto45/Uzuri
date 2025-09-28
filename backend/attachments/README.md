# Attachments Module API Documentation

## Endpoints

### Attachment
- `GET /api/attachments/attachments/` — List all attachments
- `POST /api/attachments/attachments/` — Upload attachment
- `GET /api/attachments/attachments/{id}/` — Retrieve attachment
- `PUT/PATCH /api/attachments/attachments/{id}/` — Update attachment
- `DELETE /api/attachments/attachments/{id}/` — Delete attachment
- `POST /api/attachments/attachments/{id}/soft_delete/` — Soft delete
- `POST /api/attachments/attachments/{id}/restore/` — Restore
- `POST /api/attachments/attachments/{id}/increment_download/` — Increment download count

### Attachment Audit
- `GET /api/attachments/audit/` — List all audit records (admin)

## Permissions
- Attachment: Authenticated users
- AttachmentAudit: Admin only

## Notes
- All endpoints require authentication.
- Soft delete/restore available via API and admin.
- Download count and analytics fields are tracked.
- Audit trail is available for all actions.
- Use `/swagger/` or `/redoc/` for interactive API docs.
