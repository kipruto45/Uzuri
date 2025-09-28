from django.contrib import admin

from .models import (
    Group, GroupAssignment, PeerReview, LiveSession, Guardian, StudentGuardianLink,
    AuditLog, MarketplaceItem, Purchase, DashboardWidget
)

admin.site.register(Group)
admin.site.register(GroupAssignment)
admin.site.register(PeerReview)
admin.site.register(LiveSession)
admin.site.register(Guardian)
admin.site.register(StudentGuardianLink)
admin.site.register(AuditLog)
admin.site.register(MarketplaceItem)
admin.site.register(Purchase)
admin.site.register(DashboardWidget)
