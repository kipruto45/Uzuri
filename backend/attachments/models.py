from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from io import BytesIO
from django.core.files.base import ContentFile


try:
    from PIL import Image
except ImportError:
    Image = None
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model



class Attachment(models.Model):

    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    content_type = models.CharField(max_length=128, blank=True)
    object_id = models.CharField(max_length=64, blank=True)
    related_model = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    is_confidential = models.BooleanField(default=False, db_index=True)
    download_count = models.PositiveIntegerField(default=0)
    analytics_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Versioning
    version = models.PositiveIntegerField(default=1, db_index=True)
    previous = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='next_versions')
    tags = models.ManyToManyField('attachments.AttachmentTag', blank=True, related_name='attachments')
    # Virus scan
    is_virus_free = models.BooleanField(default=True, db_index=True)
    virus_scan_report = models.TextField(blank=True)
    # Advanced features
    expiry_date = models.DateTimeField(null=True, blank=True, db_index=True)
    is_approved = models.BooleanField(default=False, db_index=True)
    download_limit = models.PositiveIntegerField(null=True, blank=True)
    shared_with_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='shared_attachments')
    shared_with_groups = models.ManyToManyField('auth.Group', blank=True, related_name='group_shared_attachments')
    file_preview = models.FileField(upload_to='attachment_previews/%Y/%m/%d/', null=True, blank=True)


# Tag for attachments
class AttachmentTag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    def __str__(self):
        return self.name

# Access log for attachments
class AttachmentAccessLog(models.Model):
    attachment = models.ForeignKey('Attachment', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} {self.action} {self.attachment} at {self.timestamp}"

# Comments on attachments
class AttachmentComment(models.Model):
    attachment = models.ForeignKey('Attachment', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user}: {self.comment[:30]}..."

# Notification log for attachments
class AttachmentNotificationLog(models.Model):
    attachment = models.ForeignKey('Attachment', on_delete=models.CASCADE)
    recipient = models.CharField(max_length=128)
    channel = models.CharField(max_length=32)
    message = models.TextField()
    status = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.recipient} via {self.channel} at {self.timestamp}"



# File preview generation logic (must be after Attachment definition)
@receiver(post_save, sender=Attachment)
def generate_file_preview(sender, instance, created, **kwargs):
    if not created:
        return
    if not instance.file:
        return
    ext = os.path.splitext(instance.file.name)[1].lower()
    preview = None
    # Image preview
    if ext in ['.jpg', '.jpeg', '.png'] and Image:
        try:
            instance.file.seek(0)
            img = Image.open(instance.file)
            img.thumbnail((300, 300))
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG')
            preview = ContentFile(thumb_io.getvalue(), name=f"preview_{instance.pk}.jpg")
        except Exception:
            pass
    # PDF preview
    elif ext == '.pdf' and fitz:
        try:
            instance.file.seek(0)
            pdf = fitz.open(stream=instance.file.read(), filetype="pdf")
            page = pdf.load_page(0)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_bytes = pix.tobytes("jpeg")
            preview = ContentFile(img_bytes, name=f"preview_{instance.pk}.jpg")
        except Exception:
            pass

