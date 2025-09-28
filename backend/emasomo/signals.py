from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    Group, GroupAssignment, PeerReview, LiveSession, AuditLog, MarketplaceItem, Purchase, DashboardWidget
)
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=GroupAssignment)
def log_group_assignment(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(user=instance.group.members.first(), action='GroupAssignmentCreated', details={'assignment': instance.assignment.id})

@receiver(post_save, sender=PeerReview)
def log_peer_review(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(user=instance.reviewer, action='PeerReviewSubmitted', details={'submission': instance.submission.id})

@receiver(post_save, sender=LiveSession)
def log_live_session(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(user=instance.created_by, action='LiveSessionCreated', details={'unit': instance.unit.id})

@receiver(post_save, sender=MarketplaceItem)
def log_marketplace_item(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(user=instance.uploaded_by, action='MarketplaceItemUploaded', details={'item': instance.id})

@receiver(post_save, sender=Purchase)
def log_purchase(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(user=instance.buyer, action='MarketplaceItemPurchased', details={'item': instance.item.id})
